/**
 * @author Rajasekhar Balla <rajasekhar.balla@kore.com>
 */
function KoreLogger(_cnf) {
    this.currentTCIndex = 0;
    this.data = {
        "botName": _cnf.botName || "Bot_Name",
        "botId": _cnf.botId || "bot_id_XXXX_XXXX_XXXX_XXXX",
        "testCases": [this.newTestCase()]
    };
};

KoreLogger.prototype.addTestCase = function () {
    this.currentTCIndex++;
    this.data.testCases.push(this.newTestCase());
};

KoreLogger.prototype.newTestCase = function () {
    return {
        "discardBefore": true,
        "name": "TC" + (this.currentTCIndex + 1),
        "messages": []
    };
};

KoreLogger.prototype.getData = function (msg, type) {
    return this.data || {};
};

KoreLogger.prototype.recordMsg = function (msg, type) {
    if(type === "botMessage"){
        if(msg && msg.message && msg.message.length && msg.message[0].component && msg.message[0].component.payload && msg.message[0].component.payload.text){
            var _botMsg = msg.message[0].component.payload.text;

            var _payload=msg.message[0].component.payload;
            if(_payload.template_type){

                //assuming template_type will have a same key to loook for values 
                var _template_key=_payload.template_type;
                if(_template_key==="button"){
                    //assumption failed for button ie..for "button" need to look "buttons"
                    _template_key="buttons";
                }
                var _obj={
                    "allOf":[_payload.text]
                }
                if(_payload && _payload[_template_key]){
                    _payload[_template_key].forEach(function(item){
                        _obj.allOf.push(item.title);
                    });
                }
                _botMsg=_obj;
            }
            this.push(_botMsg, 'botMessage');
        }  
    }else if(type === "userMessage"){
        if(msg && msg.message && msg.message.body){
            this.push(msg.message.body,type);            
        }
    }
};

KoreLogger.prototype.push = function (msg, type) {
    if (type === 'botMessage') {
        if (!this.isDiscard) {
            var _msgs = this.data.testCases[this.currentTCIndex].messages;
            var _currentMsg = _msgs[_msgs.length - 1];
            if (_currentMsg.outputs) {
                _currentMsg.outputs.push({
                    "contains": msg
                });
            } else {
                _currentMsg.outputs = [
                    {
                        "contains": msg
                    }
                ];
            }
        } else {
            this.isDiscard = false;
        }

    } else if (type === "userMessage") {
        if (msg.toLowerCase() === 'discard all') {
            this.isDiscard = true;
            this.addTestCase();
        } else {
            this.data.testCases[this.currentTCIndex].messages.push({
                "input": msg
            });
        }

    }
};

KoreLogger.prototype.writeFile = function writeFile() {
    var filename = "TestSuit.json";
    var data = JSON.stringify(this.getData());
    this.writeToFile(data,filename)
};

KoreLogger.prototype.writeToFile=function(data,filename){
    filename=filename||"File";
    if (navigator.msSaveBlob) {
        var blob = new Blob([data], { type: 'data:text/plain;charset=utf-8' });
        return window.navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(data));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }
};

KoreLogger.prototype.convertToSTR=function(data){
    var txt="";
    data.testCases.forEach(function(tc){
        txt+="\r\n-----------------"+tc.name+"\r\n\r\n";
        tc.messages.forEach(function(msg){
            txt+='user input:'+msg.input+'\r\n';
            var _botRes="";
            if(msg.outputs && msg.outputs.length){
                msg.outputs.forEach(function(output){
                    if(typeof output==="string"){
                        _botRes+=output;
                    }else if(output.contains.allOf){
                        output.contains.allOf.forEach(function(allMsg){
                            _botRes+=allMsg;
                        });
                    }else{
                        _botRes+=output.contains;
                    }
					_botRes+='\r\n';
                });
            }
            txt+='bot:'+_botRes+'';
        });
    });
    return txt;

};

KoreLogger.prototype.saveAsReadableFormat = function saveAsReadableFormat() {
    var filename = "TestSuitSTR.txt";
    var data =this.getData();
    this.writeToFile(this.convertToSTR(data),filename);
};




