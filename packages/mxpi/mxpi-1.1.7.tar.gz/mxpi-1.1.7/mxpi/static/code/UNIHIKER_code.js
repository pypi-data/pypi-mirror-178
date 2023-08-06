Blockly.Python.Dfrobot_UNIHIKER_drawtext = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var name=Blockly.Python.valueToCode(this,'TEXTS',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var size=Blockly.Python.valueToCode(this,'SIZE',Blockly.Python.ORDER_ASSIGNMENT);
    var color=this.getFieldValue('COLOR')
    var code='UNIHIKER_gui.draw_text(text='+name+',x='+x+',y='+y+',font_size='+size+', color="'+color+'")\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_draw_digit = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var name=Blockly.Python.valueToCode(this,'TEXTS',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var size=Blockly.Python.valueToCode(this,'SIZE',Blockly.Python.ORDER_ASSIGNMENT);
    var color=this.getFieldValue('COLOR')
    var code='UNIHIKER_gui.draw_digit(text='+name+',x='+x+',y='+y+',font_size='+size+', color="'+color+'")\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_draw_image = function() {
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var image=Blockly.Python.valueToCode(this,'IMAGE',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var code='UNIHIKER_gui.draw_image(image='+image+',x='+x+',y='+y+')\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_draw_emoji = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var name=this.getFieldValue('NAME')
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var time=Blockly.Python.valueToCode(this,'TIME',Blockly.Python.ORDER_ASSIGNMENT);
    var code='UNIHIKER_gui.draw_emoji(emoji="'+name+'",x='+x+',y='+y+',duration='+time+')\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_add_button = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var name=Blockly.Python.valueToCode(this,'TEXTS',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var w=Blockly.Python.valueToCode(this,'W',Blockly.Python.ORDER_ASSIGNMENT);
    var h=Blockly.Python.valueToCode(this,'H',Blockly.Python.ORDER_ASSIGNMENT);
    var ck=Blockly.Python.valueToCode(this,'CK',Blockly.Python.ORDER_ASSIGNMENT);
    var code='UNIHIKER_gui.add_button(text='+name+',x='+x+',y='+y+',w='+w+',h='+h+',onclick='+ck+')\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_draw_clock = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var l=Blockly.Python.valueToCode(this,'L',Blockly.Python.ORDER_ASSIGNMENT);
    var color=this.getFieldValue('COLOR')
    var code='UNIHIKER_gui.draw_clock(x='+x+',y='+y+',r='+l+',color="'+color+'")\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_fill_clock = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var l=Blockly.Python.valueToCode(this,'L',Blockly.Python.ORDER_ASSIGNMENT);
    var bcolor=this.getFieldValue('BCOLOR')
    var tcolor=this.getFieldValue('TCOLOR')
    var code='UNIHIKER_gui.fill_clock(x='+x+',y='+y+',r='+l+',color="'+bcolor+'",fill="'+tcolor+'")\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };

  Blockly.Python.Dfrobot_UNIHIKER_draw_qr_code = function() {
    Blockly.Python.definitions_['unihiker_GUI'] = 'from unihiker import GUI\nUNIHIKER_gui=GUI()';
    var names=Blockly.Python.valueToCode(this,'NAMES',Blockly.Python.ORDER_ASSIGNMENT);
    var text=Blockly.Python.valueToCode(this,'TEXT',Blockly.Python.ORDER_ASSIGNMENT);
    var x=Blockly.Python.valueToCode(this,'X',Blockly.Python.ORDER_ASSIGNMENT);
    var y=Blockly.Python.valueToCode(this,'Y',Blockly.Python.ORDER_ASSIGNMENT);
    var l=Blockly.Python.valueToCode(this,'L',Blockly.Python.ORDER_ASSIGNMENT);
    var code='UNIHIKER_gui.draw_qr_code(text='+text+',x='+x+',y='+y+',w='+l+')\n'
    if(names!='unnamed'){
        code=names+' = '+code
    }
    return code;
  };
