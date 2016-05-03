/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function getElementByKey(arr,key,value){
    for(var i=0;i<arr.length;++i){
        if(arr[i][key]==value)return arr[i];
    }
    return null;
}

function FormField(type){
    this.body=document.createElement("div");
    this.body.setAttribute("class","form-group");
    this.label=document.createElement("label");
    this.type=type;
    switch(type){
        case "text":
            this.input=document.createElement("input");
            this.input.setAttribute("type","text");
            this.input.setAttribute("class","form-control");
            break;
        case "selection":
            this.input=document.createElement("select");
            this.input.setAttribute("class","form-control");
            break;
    }
    this.body.appendChild(this.label);
    this.body.appendChild(this.input);
}

FormField.prototype.setVisible=function(value){
    if(value==true){
        this.body.display="";
    }else if(value==false){
        this.body.display="none";
    }
};

FormField.prototype.isVisible=function(){
    if(this.body.display=="none")return false;
    return true;
};

FormField.prototype.setId=function(id){
    this.input.setAttribute("id",id);
    this.label.setAttrivute("for",id);
};
FormField.prototype.getId=function(){
    return this.input.getAttribute("id");
};

FormField.prototype.setName=function(name){
    this.input.setAttribute("name",name);
};
FormField.prototype.getName=function(){
    return this.input.getAttribute("name");
};

FormField.prototype.setLabelText=function(text){
    this.label.innerHTML=text;
};
FormField.prototype.getLabelText=function(){
    return this.label.innerText;
};

FormField.prototype.setValue=function(value){
    if(this.type=="text"){
        this.input.value=value;
    }else if(this.type=="selection"){
        for(var i=0;i<this.input.options.length;++i){
            if(this.input.options[i].value==value){
                this.input.options[i].selected=true;
                break;
            }
        }
    }
};
FormField.prototype.getValue=function(){
    return this.input.value;
};
FormField.prototype.addOption=function(text,value){
    if(this.type=="selection"){
        var option=document.createElement("option");
        option.text=text;
        //option.value=
    }
}

function SlotBlock(serviceData,logic,slotId,constructor){
    var self=this;
    this.body=document.createElement("div");
    this.constructor=constructor;
    this.logic=logic;
    this.slotLogic=getElementByKey(logic["slots"],0,slotId);
    this.serviceData=serviceData;
    this.paramFields=[];
    this.subSlotBlocks=[];
    
    var slotInf=getElementByKey(this.serviceData["slots"],"id",this.slotLogic[0]);
    
    this.selectField=new FormField("selection");
    this.selectField.setLabelText(slotInf["name"]);
    this.selectField.setName("slot_"+slotInf["id"]);
    this.selectField.input.innerHTML="<option value='0'></option>";
    for(var i=2;i<this.slotLogic.length;++i){
        if(constructor.isActiveStrategy(this.slotLogic[i])){
            var option=document.createElement("option");
            var strategyInf=getElementByKey(this.serviceData["strategies"],"id",this.slotLogic[i]["id"]);
            option.text=strategyInf["name"];
            option.value=strategyInf["id"];
            this.selectField.input.add(option);
        }
    }
    this.selectField.setValue(0);
    this.body.appendChild(this.selectField.body);
    this.selectField.input.addEventListener("change",function(){
        self.clearParams();
        self.clearSubSlots();
        var val=self.selectField.getValue();
        if(val!=0){
            var strategyLogic=getElementByKey(self.slotLogic.slice(2),"id",val);
            if(strategyLogic["params"]!==undefined){
                for(var i=0;i<strategyLogic["params"].length;++i){
                    var param=getElementByKey(self.serviceData["params"],"id",strategyLogic["params"][i][0]);
                    var pf=new FormField("text");
                    pf.setLabelText(param["name"]);
                    pf.setName("param_"+param["id"]);
                    pf.setValue(strategyLogic["params"][i][1]);
                    self.paramFields.push(pf);
                    self.body.appendChild(pf.body);
                }
            }
            if(strategyLogic["contains"]!==undefined){
                for(var i=0;i<strategyLogic["contains"].length;++i){
                    var slot=getElementByKey(self.serviceData["slots"],"id",strategyLogic["contains"][i]);
                    var sb=new SlotBlock(self.serviceData,self.logic,slot["id"],self.constructor);
                    self.subSlotBlocks.push(sb);
                    self.body.appendChild(sb.body);
                }
            }
        }
        self.constructor.update();
    });
}
SlotBlock.prototype.getSelectedStrategy=function(){
    return this.selectField.getValue();
}
SlotBlock.prototype.hasStrategy=function(strategyId){
    if(this.getSelectedStrategy()==strategyId) return true;
    for(var i=0;i<this.subSlotBlocks.length;++i)
        if(this.subSlotBlocks[i].hasStrategy(strategyId))return true;
    return false;
}
SlotBlock.prototype.updateField=function(){
    var strategyId=this.getSelectedStrategy();
    var hasStrategyId=false;
    this.selectField.input.innerHTML="<option value='0'></option>";
    for(var i=2;i<this.slotLogic.length;++i){
        if(this.constructor.isActiveStrategy(this.slotLogic[i])){
            var option=document.createElement("option");
            var strategyInf=getElementByKey(this.serviceData["strategies"],"id",this.slotLogic[i]["id"]);
            option.text=strategyInf["name"];
            option.value=strategyInf["id"];
            if(strategyInf["id"]==strategyId)hasStrategyId=true;
            this.selectField.input.add(option);
        }
    }
    if(!hasStrategyId){
        this.clearSubSlots();
        this.clearParams();
        strategyId=0;
    }
    this.selectField.setValue(strategyId);
}
SlotBlock.prototype.clearSubSlots=function(){
    for(var i=0;i<this.subSlotBlocks.length;++i){
        this.subSlotBlocks[i].remove();
    }
    this.subSlotBlocks.length=0;
}
SlotBlock.prototype.clearParams=function(){
    for(var i=0;i<this.paramFields.length;++i){
        this.body.removeChild(this.paramFields[i].body);
    }
    this.paramFields.length=0;
}

SlotBlock.prototype.update=function(){
    this.updateField();
    for(var i=0;i<this.subSlotBlocks.length;++i){
        this.subSlotBlocks[i].update();
    }
}

SlotBlock.prototype.remove=function(){
    this.body.parentNode.removeChild(this.body);
}

/*
 * generatorData={id:"",gen_id:"",name:"",data:{"slots":[[],[]],"baseparams":[[],[]]}}
 * serviceData={"slots":[{id:"",name:""},{id:"",name:""}],"strategies":[{id:"",name:""}],"params":[{id:"",name:""}]}
 */
function AlgConstructor(generatorData,serviceData){
    this.generatorData=generatorData;
    this.serviceData=serviceData;
    this.baseParams=[];
    this.baseSlots=[];
    this.body=document.createElement("div");
    this.button=document.createElement("input");
    var temp=this.generatorData["data"];
    for(var i=0;i<temp["baseparams"].length;++i){
        var param=getElementByKey(this.serviceData["params"],"id",temp["baseparams"][i][0]);
        var pf=new FormField("text");
        pf.setLabelText(param["name"]);
        pf.setName("param_"+param["id"]);
        pf.setValue(temp["baseparams"][i][1]);
        this.baseParams.push(pf);
        this.body.appendChild(pf.body);
    }
    
    for(var i=0;i<temp["slots"].length;++i){
        if(temp["slots"][i][1]){
            var slot=getElementByKey(this.serviceData["slots"],"id",temp["slots"][i][0]);
            var slotBlock=new SlotBlock(this.serviceData,this.generatorData["data"],slot["id"],this);
            this.baseSlots.push(slotBlock);
            this.body.appendChild(slotBlock.body);
        }
    }
    this.button.setAttribute("type","submit");
    this.button.setAttribute("class","btn btn-primary btn-block");
    this.button.setAttribute("value","Сгенерировать");
    //$(this.button).click(this.onsubmit);
    this.body.appendChild(this.button);
}

AlgConstructor.prototype.isActiveStrategy=function(strategyInf){
    if(strategyInf["depends"]===undefined) return true;
    else{
        var ds=Object.keys(strategyInf["depends"]);
        if(ds.length==0) return true;
        var isActive=true;
        for(var i=0;i<ds.length && isActive;++i){
            var temp=false;
            for(var j=0;j<strategyInf["depends"][ds[i]].length && !temp;++j){
                temp=this.hasStrategy(strategyInf["depends"][ds[i]][j]);
            }
            if(!temp)isActive=false;
        }
        return isActive;
    }
    return false;
}

AlgConstructor.prototype.hasStrategy=function(strategyId){
    for(var i=0;i<this.baseSlots.length;++i){
        if(this.baseSlots[i].hasStrategy(strategyId))return true;
    }
    return false;
}

AlgConstructor.prototype.update=function(){
    for(var i=0;i<this.baseSlots.length;++i){
        this.baseSlots[i].update();
    }
}

AlgConstructor.prototype.onsubmit=function(){
    var msg   = $('form').serialize();
        $.ajax({
          type: 'POST',
          dataType:"json",
          url: window.location.href,
          data: msg,
          success: function(data) {
            window.open("/core/downloadimpls/"+data.id, '_blank')
            window.location.assign("/core/implementations/"+data.id)
          },
          error:  function(xhr, str){
        alert('Возникла ошибка: ' + xhr.responseCode);
          }
        });
}

function unique(arr){
    return arr.filter(function(item, pos) {return arr.indexOf(item) == pos;})
}

function gatherEntities(logic){
    var res={"slots":[],"params":[],"strategies":[]};
    var temp=logic["baseparams"];
    for(var i=0;i<temp.length;++i){
        res["params"].push(temp[i][0]);
    }
    
    temp=logic["slots"];
    for(var i=0;i<temp.length;++i){
        res["slots"].push(temp[i][0]);
        for(var j=2;j<temp[i].length;++j){
            var strategy=temp[i][j];
            res["strategies"].push(strategy["id"]);
            if(strategy["contains"]!==undefined){
                for(var ij=0;ij<strategy["contains"].length;++ij){
                    res["slots"].push(strategy["contains"][ij]);
                }
            }
            if(strategy["params"]!==undefined){
                for(var ij=0;ij<strategy["params"].length;++ij){
                    res["params"].push(strategy["params"][ij][0]);
                }
            }
            if(strategy["depends"]!==undefined){
                var slts=Object.keys(strategy["depends"]);
                for(var ij=0;ij<slts.length;++ij){
                    res["slots"].push(slts[ij]);
                    for(var iji=0;iji<strategy["depends"][slts[ij]].length;++iji){
                        res["strategies"].push(strategy["depends"][slts[ij]][iji]);
                    }
                }
            }
        }
    }
    res["slots"]=unique(res["slots"]);
    res["params"]=unique(res["params"]);
    res["strategies"]=unique(res["strategies"]);
    return res;
}


var restApiUrl="/api/";
function createAlgConstructorById(algConstructorId){
    var genData=null;
    $.ajax({
        type:"GET",
        async:false,
        dataType:"json",
        url: restApiUrl+"algconstructors/"+algConstructorId,
        success: function(data){
            genData=data;
            genData["data"]=JSON.parse(genData["data"]);
        }
    });
    var entities=gatherEntities(genData["data"]);
    var serviceData={"slots":null,"strategies":null,"params":null};
    $.ajax({
        type:"GET",
        async:false,
        dataType:"json",
        url: restApiUrl+"slots/?ids="+entities["slots"].join(","),
        success: function(data){
            serviceData["slots"]=data;
        }
    });
    $.ajax({
        type:"GET",
        async:false,
        dataType:"json",
        url: restApiUrl+"strategies/?ids="+entities["strategies"].join(","),
        success: function(data){
            serviceData["strategies"]=data;
        }
    });
    $.ajax({
        type:"GET",
        async:false,
        dataType:"json",
        url: restApiUrl+"algparams/?ids="+entities["params"].join(","),
        success: function(data){
            serviceData["params"]=data;
        }
    });
    return new AlgConstructor(genData,serviceData);
}