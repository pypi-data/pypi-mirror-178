

Blockly.Blocks.Dfrobot_UNIHIKER_drawtext= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("TEXTS")
        .setCheck(null)
        .appendField("显示文字");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("SIZE")
        .setCheck(null)
        .appendField("字号");
    this.appendDummyInput()
        .appendField("颜色")
        .appendField(new Blockly.FieldColour("#ff6600"), "COLOR");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示文字");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_draw_digit= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("TEXTS")
        .setCheck(null)
        .appendField("显示仿数码管字体");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("SIZE")
        .setCheck(null)
        .appendField("字号");
    this.appendDummyInput()
        .appendField("颜色")
        .appendField(new Blockly.FieldColour("#ff6600"), "COLOR");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示仿数码字体");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_draw_image= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("IMAGE")
        .setCheck(null)
        .appendField("显示图片");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示图片");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_draw_emoji= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendDummyInput()
        .appendField("显示内置动态表情")
        .appendField(new Blockly.FieldDropdown([["愤怒","Angry"],["紧张","Nerve"],["平静","Peace"],["惊讶","Shock"],["睡觉","Sleep"],["微笑","Smile"],["冒汗","Sweat"],["思考","Think"],["眨眼","Wink"]]), "NAME");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("TIME")
        .setCheck(null)
        .appendField("间隔");
    this.appendDummyInput()
        .appendField("秒");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示内置动态表情");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_add_button= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("TEXTS")
        .setCheck(null)
        .appendField("增加按钮");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("W")
        .setCheck(null)
        .appendField("宽");
    this.appendValueInput("H")
        .setCheck(null)
        .appendField("高");
    this.appendValueInput("CK")
        .setCheck(null)
        .appendField("点击回调函数");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上增加按钮");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_draw_clock= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("显示时钟")
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("L")
        .setCheck(null)
        .appendField("半径");
    this.appendDummyInput()
        .appendField("颜色")
        .appendField(new Blockly.FieldColour("#ff6600"), "COLOR");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示时钟");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_fill_clock= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("显示填充时钟")
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("L")
        .setCheck(null)
        .appendField("半径");
    this.appendDummyInput()
        .appendField("边框颜色")
        .appendField(new Blockly.FieldColour("#ff6600"), "BCOLOR");
    this.appendDummyInput()
        .appendField("填充颜色")
        .appendField(new Blockly.FieldColour("#ff6600"), "TCOLOR");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示内置动态表情");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.Dfrobot_UNIHIKER_draw_qr_code= {
    init: function() {
    this.appendValueInput("NAMES")
        .setCheck(null)
        .appendField(new Blockly.FieldImage("./static/media/ulogo.png", 20, 20, "*"))
        .appendField("对象名");
    this.appendValueInput("TEXT")
        .setCheck(null)
        .appendField("显示二维码 内容");
    this.appendValueInput("X")
        .setCheck(null)
        .appendField("在X");
    this.appendValueInput("Y")
        .setCheck(null)
        .appendField("Y");
    this.appendValueInput("L")
        .setCheck(null)
        .appendField("边长");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('UNIHIKER_blocks');
    this.setTooltip("在行空板上显示内置动态表情");
    this.setHelpUrl("");
    }
  };