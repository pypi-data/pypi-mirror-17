/* Javascript */
var M = {};

Vue.config.delimiters = ['${', '}'];
var vm = new Vue({
  el: '#main-content',
  data: {
    landscape: false,
    latest_screen: null,
    screen_scale: null,
    android_serials: [],
    device: {
      platform: 'android',
      ios_url: '',
      serial: '',
    },
  },
  methods: {
    toggleLandscape: function() {
      this.landscape = !this.landscape;
    },
    connectDevice: function(){
      var serial = this.device.platform == 'ios' ? this.device.ios_url : this.device.serial;
      console.log("connecting", this.device.platform, serial);
      $.ajax({
        url: '/device',
        method: 'POST',
        dataType: 'json',
        data: {
          serial: serial,
        },
        success: function(data){
          $.notify('连接成功, 刷新中..', {position: 'top center', className: 'success'});
          // TODO: update device info
          console.log(123, data);
          $('#btn-refresh-screen').click();
          $('#device-chooser').hide();
        },
        error: function(err) {
          $.notify('连接失败', {position: 'top center', className: 'error'});
          $('#device-chooser').show();
        }
      });
    },
    cancelConnectDevice: function(){
      $('#device-chooser').hide();
    },
  },
})

$(function(){
  var blocklyDiv = document.getElementById('blocklyDiv');
  var workspace = Blockly.inject(blocklyDiv,
    {toolbox: document.getElementById('toolbox')});
  Blockly.Python.STATEMENT_PREFIX = 'highlight_block(%1);\n';
  Blockly.Python.addReservedWords('highlight_block');
  M.workspace = workspace;

  var RUN_BUTTON_TEXT = {
    'ready': '<span class="glyphicon glyphicon-play"></span> 运行</a>',
    'running': '<span class="glyphicon glyphicon-stop"></span> 停止</a>',
  }

  // Initial global value for blockly images
  window.blocklyBaseURL = 'http://'+ location.host +'/static_imgs/';
  window.blocklyImageList = null;
  window.blocklyCropImageList = null;

  //  useless
  // $.getJSON('/api/images', function(res){
  //   window.blocklyImageList = res.images;
  //   window.blocklyBaseURL = res.baseURL;
  // })


  function changeRunningStatus(status, message){
    M.runStatus = status;
    var $play = $('a[href=#play]');
    if (message) {
      $play.notify(message, {className: 'success', position: 'top'});
    }
    if (status){
      $play.html(RUN_BUTTON_TEXT[status]);
    }
  }

  function connectWebsocket(){
    var ws = new WebSocket('ws://'+location.host+'/ws')
    M.ws = ws;

    ws.onopen = function(){
      ws.send(JSON.stringify({command: "refresh"}))
      $.notify(
        '与后台通信连接成功!!!',
        {position: 'top center', className: 'success'});
      getDeviceChoices();
    };
    ws.onmessage = function(evt){
      try {
        var data = JSON.parse(evt.data)
        console.log(evt.data);
        switch(data.type){
        case 'image_list':
          M.images = data.images;
          window.blocklyImageList = [];
          $('#imagesDiv>ul').empty();
          for (var i = 0, info; i < data.images.length; i++) {
            info = data.images[i];
            window.blocklyImageList.push([info['name'], info['path']]);
            $('#imagesDiv>ul')
              .append($('<li>')
                      .append($('<div>')
                            .append($('<img>').attr('src', window.blocklyBaseURL + info['path']))
                            .append($('<p>').text(info['name']))
                      )
              );
          }
          window.blocklyCropImageList = [];
          for (var i = 0, info; i < data.screenshots.length; i++) {
            info = data.screenshots[i]
            window.blocklyCropImageList.push([info['name'], info['path']]);
          }
          vm.latest_screen = data.latest;
          $('#btn-image-refresh').notify(
            '已刷新',
            {className: 'success', position: 'right'}
          );
          restoreWorkspace();
          break;
        case 'run':
          changeRunningStatus(data.status, data.notify);
          break;
        case 'stop':
          changeRunningStatus(data.status, data.notify);
          break;
        case 'traceback':
          alert(data.output);
          break;
        case 'highlight':
          var id = data.id;
          workspace.highlightBlock(id)
          break;
        case 'console':
          var $console = $('pre.console');
          var text = $console.html();
          $console.text($console.html() + data.output);
          $console.scrollTop($console.prop('scrollHeight'));
        default:
          console.log("No match data type: ", data.type)
        }
      }
      catch(err){
        console.log(err, evt.data)
      }
    };
    ws.onerror = function(err){
      // $.notify(err);
      // console.error(err)
    };
    ws.onclose = function(){
      console.log("Closed");
      $.notify(
        '与后台通信连接断开, 2s钟后重新连接 !!!',
        {position: 'top center', className: 'error'})
      setTimeout(function(){
        connectWebsocket()
      }, 2000)
    };
  }
  connectWebsocket()

  function generateCode(workspace) {
    var xml = Blockly.Xml.workspaceToDom(workspace);
    Blockly.Python.STATEMENT_PREFIX = '';
    var pythonText = Blockly.Python.workspaceToCode(workspace);

    Blockly.Python.STATEMENT_PREFIX = 'highlight_block(%1);\n';
    var pythonDebugText = Blockly.Python.workspaceToCode(workspace);

    return {
      xmlText: Blockly.Xml.domToPrettyText(xml),
      pythonText: pythonText,
      pythonDebugText: pythonDebugText,
    }
  }

  function saveWorkspace(callback) {
    var $this = $('a[href=#save]');
    var originHtml = $this.html();
    $this.html('<span class="glyphicon glyphicon-floppy-open"></span> 保存')

    var g = generateCode(workspace);
    $.ajax({
      url: '/workspace',
      method: 'POST',
      data: {'xml_text': g.xmlText, 'python_text': g.pythonText},
      success: function(e){
        // console.log(e);
        // $this.html('<span class="glyphicon glyphicon-floppy-open"></span> 已保存')
        $('a[href=#save]').notify('保存成功',
          {className: 'success', position: 'left', autoHideDelay: 700});
      },
      error: function(e){
        console.log(e);
        $this.notify(e.responseText || '保存失败，请检查服务器连接是否正常',
          {className: 'warn', elementPosition: 'left', autoHideDelay: 5000});
      },
      complete: function(){
        $this.html(originHtml)
        $('.code-python').text(g.pythonText);
        if (callback){
          callback(g)
        }
      }
    })
  }

  function updateGenerate(workspace) {
    var g = generateCode(workspace);
    $('.code-python').text(g.pythonText);
  }

  function updateFunction(event) {
    updateGenerate(workspace)
    if (updateFunction.timeoutKey) {
      clearTimeout(updateFunction.timeoutKey);
    }
    updateFunction.timeoutKey = setTimeout(saveWorkspace, 1400);
  }

  function restoreWorkspace() {
    // do nothing if not visible.
    if ($('#blocklyDiv').css('display') == 'none') {
      return;
    }
    $.get('/workspace')
      .success(function(res){
        var xml = Blockly.Xml.textToDom(res.xml_text);
        // clear up before add
        workspace.clear();
        Blockly.Xml.domToWorkspace(workspace, xml);
        updateGenerate(workspace)
      })
      .error(function(res){
        alert(res.responseText);
      })
      .complete(function(){
        setTimeout(function(){
          updateFunction();
          //workspace.addChangeListener(updateFunction);
        }, 700)
      })
  }

  function sendWebsocket(message){
    var data = JSON.stringify(message);
    M.ws.send(data);
  }

  $('a[href=#save]').click(function(event){
    event.preventDefault();
    saveWorkspace()
  })

  $('a[href=#play]').click(function(event){
    event.preventDefault();
    console.log("Click play")
    M.workspace.traceOn(true); // enable step run
    var g = generateCode(workspace);
    var isPlay = M.runStatus == 'running';
    sendWebsocket({command: (isPlay ? 'stop' : 'run'), code: g.pythonDebugText})
  })

  $('.btn-clear-console').click(function(){
    $('pre.console').text('');
  })

  $('li[role=presentation]').click(function(){
    var text = $.trim($(this).text());
    M.workspace.setVisible(text === 'Blockly');
    setTimeout(function () {
      Blockly.svgResize(M.workspace);
    }, 10);
  })

  $('#btn-save-screen').click(function(){
    if (crop_bounds.bound === null) {
      $.notify('还没选择截图区域！');
      return;
    }
    var filename = window.prompt('保存的文件名, 不需要输入.png扩展名');
    if (!filename){
      return;
    }
    filename = filename + '.png';
    $.ajax({
      url: '/images/screenshot',
      method: 'POST',
      dataType: 'json',
      data: {
        screenname: vm.latest_screen,
        filename: filename,
        bound: crop_bounds.bound,
      },
      success: function(res){
        console.log(res)
        $.notify('图片保存成功', 'success')
        sendWebsocket({command: 'refresh'})
        $('#screen-crop').css({'left':'0px', 'top':'0px','width':'0px', 'height':'0px'});
      },
      error: function(err){
        console.log(err)
        $.notify('图片保存失败，打开调试窗口查看具体问题')
      },
    })
  })

  $('#btn-refresh-screen').click(function(){
    M.screenURL = '/images/screenshot?v=t' + new Date().getTime();
    var $this = $(this);
    $this.notify('Refreshing', {className: 'info', position: 'top'})
    $this.prop('disabled', true);

    loadCanvasImage(M.canvas, M.screenURL, function(err){
      if (err){
        $this.notify(err, 'error')
        getDeviceChoices();
      }
      $this.prop('disabled', false);
      sendWebsocket({command: 'refresh'})
    })
  })

  function getDeviceChoices(){
    $.ajax({
      url: '/device',
      method: 'GET',
      dataType: 'json',
      data: {
        platform: vm.device.platform,
      },
      success: function(data){
        // clean old devices
        vm.android_serials.splice(0, vm.android_serials.length);
        for (var i = 0, s; i < data.android.length; i++) {
          s = data.android[i];
          vm.android_serials.push(s);
        }
        $('#device-chooser').show();
      },
      error: function(err) {
        console.log(222, err);
      }
    });
  }

  $('#btn-change-device').click(function(){
    getDeviceChoices();
  });


  $('.fancybox').fancybox()

  function getPageHeight(){
    return document.documentElement.clientHeight;
  }

  function resizeCanvas(canvas){
    var width = $('#screen-wrapper').width();
    canvas.setAttribute('width', width);
    canvas.setAttribute('height', width*(M.screenRatio || 1.78));
    // loadCanvasImage(canvas, M.screenURL);
  }

  function loadCanvasImage(canvas, url, callback){
    var context = canvas.getContext('2d')
    var imageObj = new Image();
    url = url || M.screenURL;
    imageObj.crossOrigin="anonymous";
    imageObj.onload = function(){
      M.screenRatio = imageObj.height / imageObj.width;
      M.screenScale = canvas.width/imageObj.width; // global
      var height = Math.floor(M.screenScale*imageObj.height);
      canvas.setAttribute('height', height);
      context.drawImage(imageObj, 0, 0, canvas.width, canvas.height);
      var $wrapper = $(canvas).parent('div')
      $wrapper.height(height);
      if (callback) {
        callback()
      }
    }
    imageObj.onerror = function(){
      if (callback){
        callback("Refresh failed.")
      }
    }
    imageObj.src = url;
  }

  function writeMessage(canvas, message) {
    var context = canvas.getContext('2d');
    context.font = '18pt Calibri';
    context.fillStyle = 'black';
    context.fillText(message, 10, 25);
  }

  function onResize(){
    var blocklyDivHeight = getPageHeight() - $("#blocklyDiv").offset().top;
    console.log($("#console-left").height())
    if (!$('#console-left').is(':hidden')){
      blocklyDivHeight -= $("#console-left").height() + 20;
    }
    console.log("blockly height:", blocklyDivHeight)
    $('#blocklyDiv').height(blocklyDivHeight-5);
    Blockly.svgResize(M.workspace);
    resizeCanvas(M.canvas);
  }

  M.canvas = document.getElementById('canvas');
  M.screenURL = '/images/screenshot?v=t' + new Date().getTime();
  window.addEventListener('resize', onResize, false);
  onResize();

  function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: Math.floor((evt.clientX - rect.left) / M.screenScale),
      y: Math.floor((evt.clientY - rect.top) / M.screenScale),
    };
  }

  var canvas = document.getElementById('canvas');
  canvas.addEventListener('mousemove', function(evt) {
    var mousePos = getMousePos(canvas, evt);
    var message = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
    // writeMessage(canvas, message);
    $('.status-bar>span').text(message);
    // console.log(message);
  }, false);

  // $("#console-left").hide(function(){
    // console.log("HE")
    // onResize(); //Blockly.fireUiEvent(window, 'resize');
  // });

  //------------ canvas overlay parts ------------//
  function getCanvasPos(x, y) {
      var left = M.screenScale * x,
          top  = M.screenScale * y;
      return {left, top};
  }

  var overlays = {
    "atx_click" : {
      $el: $('<div>').addClass('point').hide().appendTo('#screen-overlays'),
      update: function(data){
        var pos = getCanvasPos(data.x, data.y);
        this.$el.css('left', pos.left+'px')
                .css('top', pos.top+'px');
      },
    },
    "atx_click_image" : {
      $el: $('<div>').addClass('image-rect').hide().appendTo('#screen-overlays')
          .append($('<div>').addClass('point')),
      update: function(data){
        var p1 = getCanvasPos(data.x1, data.y1),
            p2 = getCanvasPos(data.x2, data.y2),
            width = p2.left - p1.left,
            height = p2.top - p1.top;
        this.$el.css('left', p1.left+'px')
                .css('top', p1.top+'px')
                .css('width', width+'px')
                .css('height', height+'px');
        this.$el.children().css('left', (data.c.x+50)+'%').css('top', (data.c.y+50)+'%');
      },
    },
    "atx_click_ui" : {
      $el: $('<div>').addClass('ui-rect').hide().appendTo('#screen-overlays'),
      update: function(data){
        var p1 = getCanvasPos(data.x1, data.y1),
            p2 = getCanvasPos(data.x2, data.y2),
            width = p2.left - p1.left,
            height = p2.top - p1.top;
        this.$el.css('left', p1.left+'px')
                .css('top', p1.top+'px')
                .css('width', width+'px')
                .css('height', height+'px');
      },
    },
    "atx_swipe" : {
      $el: $('#overlays-swipe').addClass('full').hide(),
      update: function(data){
        var p1 = getCanvasPos(data.x1, data.y1),
            p2 = getCanvasPos(data.x2, data.y2);
        var $svg = this.$el.children('svg'),
            cstart = '<circle cx="'+p1.left+'" cy="'+p1.top+'" fill="black" r="3"></circle>'
            cend = '<circle cx="'+p2.left+'" cy="'+p2.top+'" fill="white" r="3"></circle>'
            line = '<line stroke="black" stroke-width="2"' +
                   ' x1="'+p1.left+'" y1="'+p1.top +
                   '" x2="'+p2.left+'" y2="'+p2.top+'"></line>';
        $svg.html(cstart + line + cend);
      },
    },
  };

  //------------ canvas do different things for different block ------------//

  // -------- selected is null, used for save screen crop -------
  var crop_bounds = {start: null, end: null, bound:null},
      crop_rect_bounds = {start:null, end:null, bound:null},
      draw_rect = false;

  // Alt: 18, Ctrl: 17, Shift: 16
  // $('body').on('keydown', function(evt){
  //   if (true || evt.keyCode != 18) {return;}
  //   draw_rect = true;
  //   crop_bounds.start = crop_bounds.end = crop_bounds.bound = null;
  //   // $("#screen-crop").css({'left':'0px', 'top':'0px', 'width':'0px', 'height':'0px'});
  // });
  // $('body').on('keyup', function(evt){
  //   if (evt.keyCode != 18) {return;}
  //   draw_rect = false;
  //   crop_rect_bounds.start = crop_rect_bounds.end = crop_rect_bounds.bound = null;
  //   // $("#screen-crop-rect").css({'left':'0px', 'top':'0px', 'width':'0px', 'height':'0px'});
  // });

  canvas.addEventListener('mousedown', function(evt){
    var blk = Blockly.selected;
    if (blk !== null) {
      return;
    }
    if (draw_rect) {
      crop_rect_bounds.start = evt;
      crop_rect_bounds.end = null;
    } else {
      crop_bounds.start = evt;
      crop_bounds.end = null;
    }
  });
  canvas.addEventListener('mousemove', function(evt){
    // ignore fake move
    if (evt.movementX == 0 && evt.movementY == 0) {
      return;
    }
    var blk = Blockly.selected;
    if (blk !== null || (crop_bounds.start == null && crop_rect_bounds.start == null)) {
      return;
    }
    var rect = canvas.getBoundingClientRect(),
        $rect, bounds;
    if (draw_rect) {
      crop_rect_bounds.end = evt;
      bounds = crop_rect_bounds;
      $rect = $("#screen-crop-rect");
    } else {
      crop_bounds.end = evt;
      bounds = crop_bounds;
      $rect = $("#screen-crop");
    }
    // update rect position
    var left = bounds.start.pageX - rect.left,
        top = bounds.start.pageY - rect.top,
        width = Math.max(bounds.end.pageX - bounds.start.pageX, 10),
        height = Math.max(bounds.end.pageY - bounds.start.pageY, 10);
    $rect.show();
    $rect.css('left', left+'px')
         .css('top', top+'px')
         .css('width', width+'px')
         .css('height', height+'px');
  });
  canvas.addEventListener('mouseup', function(evt){
    var blk = Blockly.selected;
    if (blk !== null) {
      return;
    }
    if  (crop_bounds.end !== null) {
      var start = getMousePos(canvas, crop_bounds.start),
          end = getMousePos(canvas, crop_bounds.end);
      crop_bounds.bound = [start.x, start.y, end.x, end.y];
    }
    crop_bounds.start = null;
    crop_rect_bounds.start = null;
  });
  canvas.addEventListener('mouseout', function(evt){
    var blk = Blockly.selected;
    if (blk !== null) {
      return;
    }
    if  (crop_bounds.start !==null && crop_bounds.end !== null) {
      var start = getMousePos(canvas, crop_bounds.start),
          end = getMousePos(canvas, crop_bounds.end);
      crop_bounds.bound = [start.x, start.y, end.x, end.y];
    }
    crop_bounds.start = null;
    crop_rect_bounds.start = null;
  });

  // -------- selected is atx_click ----------
  canvas.addEventListener('click', function(evt){
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_click') {
      return;
    }
    // update model in blockly
    var pos = getMousePos(this, evt);
    var rect = canvas.getBoundingClientRect();
    blk.setFieldValue(pos.x, 'X');
    blk.setFieldValue(pos.y, 'Y');
    // update point position
    var $point = overlays['atx_click'].$el;
    $point.css('left', (evt.pageX-rect.left)+'px').css('top', (evt.pageY-rect.top)+'px');
  });

  // --------- selected is atx_click_image ------------
  var rect_bounds = {start: null, end: null};
  canvas.addEventListener('mousedown', function(evt){
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_click_image') {
      return;
    }
    rect_bounds.start = evt;
    rect_bounds.end = null;
  });
  canvas.addEventListener('mousemove', function(evt){
    // ignore fake move
    if (evt.movementX == 0 && evt.movementY == 0) {
      return;
    }
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_click_image' || rect_bounds.start == null) {
      return;
    }
    rect_bounds.end = evt;
    // update model in blockly
    var pat_conn = blk.getInput('ATX_PATTERN').connection.targetConnection;
    if (pat_conn == null) { return;}
    var pat_blk = pat_conn.sourceBlock_;
    if (pat_blk.type != 'atx_image_pattern_offset') {return;}
    var img_conn = pat_blk.getInput('FILENAME').connection.targetConnection;
    if (img_conn == null) { return;}
    var img_blk = img_conn.sourceBlock_;
    if (img_blk.type != 'atx_image_crop_preview') {return; }
    var crop_conn = img_blk.getInput('IMAGE_CROP').connection.targetConnection;
    if (crop_conn == null) { return;}
    var crop_blk = crop_conn.sourceBlock_,
        start_pos = getMousePos(this, rect_bounds.start),
        end_pos = getMousePos(this, rect_bounds.end);
    crop_blk.setFieldValue(start_pos.x, 'LEFT');
    crop_blk.setFieldValue(start_pos.y, 'TOP');
    crop_blk.setFieldValue(end_pos.x - start_pos.x, 'WIDTH');
    crop_blk.setFieldValue(end_pos.y - start_pos.y, 'HEIGHT');
    pat_blk.setFieldValue(0, 'OX');
    pat_blk.setFieldValue(0, 'OY');

    // update image-rect position
    var $rect = overlays['atx_click_image'].$el,
        rect = canvas.getBoundingClientRect(),
        left = rect_bounds.start.pageX,
        top = rect_bounds.start.pageY,
        width = Math.max(rect_bounds.end.pageX - left, 10),
        height = Math.max(rect_bounds.end.pageY - top, 10);
    $rect.css('left', (left-rect.left)+'px')
         .css('top', (top-rect.top)+'px')
         .css('width', width+'px')
         .css('height', height+'px');
    $rect.children().css('left', '50%').css('top', '50%');
  });
  canvas.addEventListener('mouseup', function(evt){
    var blk = Blockly.selected;
    // mouseup event should only be triggered when there happened mousemove
    if (blk == null || blk.type != 'atx_click_image' || rect_bounds.end == null) {
      return;
    }
    rect_bounds.start = null;
  });
  canvas.addEventListener('mouseout', function(evt){
    var blk = Blockly.selected;
    // mouseout is same as mouseup
    if (blk == null || blk.type != 'atx_click_image' || rect_bounds.end == null) {
      return;
    }
    rect_bounds.start = null;
  });
  canvas.addEventListener('click', function(evt){
    var blk = Blockly.selected;
    // click event should only be triggered when there's no mousemove happened.
    if (blk == null || blk.type != 'atx_click_image' || rect_bounds.end != null) {
      return;
    }
    rect_bounds.start = null;
    // update model in blockly
    var pat_conn = blk.getInput('ATX_PATTERN').connection.targetConnection;
    if (pat_conn == null) { return;}
    var pat_blk = pat_conn.sourceBlock_;
    if (pat_blk.type !== 'atx_image_pattern_offset') {return;}

    // update image-rect point position
    var $rect = overlays['atx_click_image'].$el,
        pos = $rect.position(),
        x = pos.left,
        y = pos.top,
        w = $rect.width(),
        h = $rect.height(),
        cx = x + w/2,
        cy = y + h/2,
        ox = parseInt((evt.pageX - cx)/w * 100),
        oy = parseInt((evt.pageY - cy)/h * 100),
        $point = $rect.children();
    pat_blk.setFieldValue(ox, 'OX');
    pat_blk.setFieldValue(oy, 'OY');
    $point.css('left', (50+ox)+'%').css('top', (50+oy)+'%');
  });

  // TODO ------------ selected is atx_click_ui ------------
  // canvas.addEventListener('click', function(evt){
  //   var blk = Blockly.selected;
  //   if (blk == null || blk.type != 'atx_click_ui') { return; }
  // });

  // ------------ selected is atx_swipe -----------
  var swipe_points = {start:null, end:null};
  canvas.addEventListener('mousedown', function(evt){
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_swipe') { return; }
    swipe_points.start = evt;
    swipe_points.end = null;
  });
  canvas.addEventListener('mousemove', function(evt){
    if (evt.movementX == 0 && evt.movementY == 0) { return; }
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_swipe' || swipe_points.start == null) { return; }
    swipe_points.end = evt;
    var spos = getMousePos(this, swipe_points.start),
        epos = getMousePos(this, swipe_points.end);
        p1 = getCanvasPos(spos.x, spos.y),
        p2 = getCanvasPos(epos.x, epos.y);
    // update blockly model
    blk.setFieldValue(spos.x, 'SX');
    blk.setFieldValue(spos.y, 'SY');
    blk.setFieldValue(epos.x, 'EX');
    blk.setFieldValue(epos.y, 'EY');
    // update line
    var $svg = $("#overlays-swipe").children('svg'),
        cstart = '<circle cx="'+p1.left+'" cy="'+p1.top+'" fill="black" r="3"></circle>'
        cend = '<circle cx="'+p2.left+'" cy="'+p2.top+'" fill="white" r="3"></circle>'
        line = '<line stroke="black" stroke-width="2"' +
               ' x1="'+p1.left+'" y1="'+p1.top +
               '" x2="'+p2.left+'" y2="'+p2.top+'"></line>';
    $svg.html(cstart + line + cend);
  });
  canvas.addEventListener('mouseup', function(evt){
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_swipe') { return; }
    swipe_points.start = null;
    swipe_points.end = null;
  });
  canvas.addEventListener('mouseout', function(evt){
    var blk = Blockly.selected;
    if (blk == null || blk.type != 'atx_swipe') { return; }
    swipe_points.start = null;
    swipe_points.end = null;
  });

  //------------ canvas show rect/points for special block ------------//
  function getBlockOverlayData(blk) {
    switch (blk.type) {
      // return {x, y}
      case 'atx_click':
        var x = parseInt(blk.getFieldValue('X')),
            y = parseInt(blk.getFieldValue('Y'));
        if (x != null && y != null) {
          return {x, y};
        } else {
          return null;
        }
      // return {x1, y1, x2, y2, c}
      case 'atx_click_image':
        var pat_conn = blk.getInput('ATX_PATTERN').connection.targetConnection;
        if (pat_conn == null) { return null;}
        var pat_blk = pat_conn.sourceBlock_;
        if (pat_blk.type != 'atx_image_pattern_offset') {return null;}
        var img_conn = pat_blk.getInput('FILENAME').connection.targetConnection;
        if (img_conn == null) { return null;}
        var img_blk = img_conn.sourceBlock_;
        if (img_blk.type != 'atx_image_crop_preview') {return null;}
        var crop_conn = img_blk.getInput('IMAGE_CROP').connection.targetConnection;
        if (crop_conn == null) { return null;}
        var imagename = img_blk.getFieldValue('IMAGE'),
            crop_blk = crop_conn.sourceBlock_,
            left = parseInt(crop_blk.getFieldValue('LEFT')),
            top = parseInt(crop_blk.getFieldValue('TOP')),
            width = parseInt(crop_blk.getFieldValue('WIDTH')),
            height = parseInt(crop_blk.getFieldValue('HEIGHT')),
            ox = parseInt(pat_blk.getFieldValue('OX')),
            oy = parseInt(pat_blk.getFieldValue('OY'));
            return {x1: left, y1: top, x2: left+width, y2: top+height, c:{x:ox, y:oy}};
      // TODO return {x1, y1, x2, y2}
      case 'atx_click_ui':
      // return {x1, y1, x2, y2}
      case 'atx_swipe':
        var x1 = parseInt(blk.getFieldValue('SX')),
            y1 = parseInt(blk.getFieldValue('SY')),
            x2 = parseInt(blk.getFieldValue('EX')),
            y2 = parseInt(blk.getFieldValue('EY'));
            return {x1, y1, x2, y2};
      default:
        return null;
    }
  }

  function hideOverlayPart(type) {
    if (!overlays.hasOwnProperty(type)) {return;}
    var obj = overlays[type];
    obj.$el.hide();
  }

  function showOverlayPart(type, blk) {
    if (!overlays.hasOwnProperty(type)) {return;}
    var obj = overlays[type];
    var data = getBlockOverlayData(blk)
    if (data != null) {
      obj.update(data);
      obj.$el.show();
    }
  }

  function onUISelectedChange(evt){
    if (evt.type != Blockly.Events.UI || evt.element != 'selected') {return;}
    if (evt.oldValue != null) {
      var oldblk = workspace.getBlockById(evt.oldValue);
      if (oldblk === null) { return;}
      hideOverlayPart(oldblk.type);
    } else {
      $('#screen-crop').hide();
      $('#btn-save-screen').attr('disabled', 'disabled');
    }
    if (evt.newValue != null) {
      var newblk = workspace.getBlockById(evt.newValue);
      showOverlayPart(newblk.type, newblk);
      useBlockScreen(newblk);
    } else {
      useBlockScreen();
      crop_bounds.bound = null;
      $('#screen-crop').css({'left':'0px', 'top':'0px',
          'width':'0px', 'height':'0px'}).show();
      $('#btn-save-screen').removeAttr('disabled');
    }
  }
  workspace.addChangeListener(onUISelectedChange);

  // track screenshot related to each block
  var block_screen = {};
  function useBlockScreen(blk) {
    var conn;
    if (blk && blk.type == 'atx_click_image') {
      conn = blk.getInput('ATX_PATTERN').connection.targetConnection;
      blk = conn && conn.sourceBlock_;
    }
    if (blk && blk.type == 'atx_image_pattern_offset') {
      conn = blk.getInput('FILENAME').connection.targetConnection;
      blk = conn && conn.sourceBlock_;
    }
    if (blk && blk.type == 'atx_image_crop_preview') {
      conn = blk.getInput('IMAGE_CROP').connection.targetConnection;
      blk = conn && conn.sourceBlock_;
    }
    var screen = blk && block_screen[blk.id] || vm.latest_screen,
        url = window.blocklyBaseURL + screen;
    if (url != M.canvas.src) {
      loadCanvasImage(M.canvas, window.blocklyBaseURL + screen);
    }
  }

  function onUIFieldChange(evt) {
    if (evt.type != Blockly.Events.CHANGE || evt.element != 'field') {return;}
    var blk = workspace.getBlockById(evt.blockId);
    if (blk.type == 'atx_image_crop' && evt.name == 'FILENAME') {
      block_screen[evt.blockId] = evt.newValue;
    }
  }
  function onCreateBlock(evt){
    if (evt.type != Blockly.Events.CREATE) {return;}
    for (var i = 0, bid; i < evt.ids.length; i++) {
      bid = evt.ids[i];
      var blk = workspace.getBlockById(bid);
      if (blk.type == 'atx_image_crop') {
        block_screen[bid] = blk.getFieldValue('FILENAME');
      }
    }
  }
  function onDeleteBlock(evt){
    if (evt.type != Blockly.Events.DELETE) {return;}
    for (var i = 0, bid; i < evt.ids.length; i++) {
      bid = evt.ids[i];
      delete block_screen[bid];
    }
  }
  function onBlockConnectionChange(evt) {
    if (evt.type != Blockly.Events.MOVE && !evt.oldParentId && !evt.newParentId) {
      return;
    }
    var oldblk = evt.oldParentId ? workspace.getBlockById(evt.oldParentId) : null,
        newblk = evt.newParentId ? workspace.getBlockById(evt.newParentId) : null;
    if (oldblk) {

    }
    if (newblk) {

    }
  }
  workspace.addChangeListener(onCreateBlock);
  workspace.addChangeListener(onDeleteBlock);
  workspace.addChangeListener(onUIFieldChange);
  workspace.addChangeListener(onBlockConnectionChange);

})
