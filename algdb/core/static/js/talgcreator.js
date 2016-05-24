

function getElementByKey(arr,key,value){
    for(var i=0;i<arr.length;++i){
        if(arr[i][key]==value)return arr[i];
    }
    return null;
}

function intTypeToString(typeId){
    arr=["int","double","bool","string","date","time","datetime","file"];
    return arr[typeId];
}

var restApiUrl="/api/";
function TemplAlgCreator(){
    var self=this;
    this.form=document.getElementById("addtalgform");
    this.talgnameInput=document.getElementById("talgname");

    this.selectedOpTable=document.getElementById("selectedops");
    this.addOpButton=document.getElementById("addopbutton");
    $(this.addOpButton).click(function(event){self.addOpButtonClicked();});

    this.selectedParamTable=document.getElementById("selectedparams");
    this.addParamButton=document.getElementById("addparambutton");
    $(this.addParamButton).click(function(event){self.addParamButtonClicked();});


    this.addTemplAlgButton=document.getElementById("addtalgbutton");

    this.addOpDialog=document.getElementById("addopdialog");
    this.selectOpDialog=document.getElementById("selectopdialog");
    this.selectOpDialogSearchInput=this.selectOpDialog.getElementsByTagName("input")[0];
    this.selectOpDialogSearchButton=this.selectOpDialog.getElementsByTagName("button")[1];
    $(this.selectOpDialogSearchButton).click(function(event){
        self.findOpsSelectOpDialog(self.selectOpDialogSearchInput.value);
    });
    $(this.selectOpDialogSearchInput).keypress(function (e) {if (e.which == 13) {
        self.findOpsSelectOpDialog(self.selectOpDialogSearchInput.value);
    }});
    this.selectOpDialogTable=this.selectOpDialog.getElementsByTagName("table")[0];

    this.addParamDialog=document.getElementById("addparamdialog");
    this.selectParamDialog=document.getElementById("selectparamdialog");
    this.selectParamDialogSearchInput=this.selectParamDialog.getElementsByTagName("input")[0];
    this.selectParamDialogSearchButton=this.selectParamDialog.getElementsByTagName("button")[1];
    $(this.selectParamDialogSearchButton).click(function(event){
        self.findParamsSelectParamDialog(self.selectParamDialogSearchInput.value);
    });
    $(this.selectParamDialogSearchInput).keypress(function (e) {if (e.which == 13) {
        self.findParamsSelectOpDialog(self.selectParamDialogSearchInput.value);
    }});
    this.selectParamDialogTable=this.selectParamDialog.getElementsByTagName("table")[0];

    this.searchedOps=[];
    this.searchedParams=[];
    this.operators=[];
    this.params=[];
}


TemplAlgCreator.prototype.addOpButtonClicked=function(){
    this.clearSearchedOpDialogTable();
    this.selectOpDialogSearchInput.value="";
    this.findOpsSelectOpDialog("");
    $(this.selectOpDialog).modal("show");
}
TemplAlgCreator.prototype.addParamButtonClicked=function(){
    this.clearSearchedParamDialogTable();
    this.selectParamDialogSearchInput.value="";
    this.findParamsSelectParamDialog("");
    $(this.selectParamDialog).modal("show");
}

TemplAlgCreator.prototype.clearSearchedOpDialogTable=function(){
    var rows=this.selectOpDialogTable.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    for(var i=rows.length-1;i>=0;--i){
        rows[i].parentNode.removeChild(rows[i]);
    }
}

TemplAlgCreator.prototype.clearSearchedParamDialogTable=function(){
    var rows=this.selectParamDialogTable.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
    for(var i=rows.length-1;i>=0;--i){
        rows[i].parentNode.removeChild(rows[i]);
    }
}

TemplAlgCreator.prototype.findOpsSelectOpDialog=function(str){
    var self=this;
    this.searchedOps=[];
    $.ajax({
        type:"GET",
        async:false,
        dataType:"json",
        url: restApiUrl+"strategies/"+(str.length>0 ? ("?name="+str) : ""),
        success: function(data){
            self.searchedOps=data;
        }
    });
    this.clearSearchedOpDialogTable();
    var tbody=this.selectOpDialogTable.getElementsByTagName("tbody")[0];
    for(var i=0;i<this.searchedOps.length;++i){
        tbody.appendChild($("<tr class='clickable-row' data-id='"+this.searchedOps[i].id+"'> <td>"+this.searchedOps[i].id+"</td><td>"+this.searchedOps[i].name+"</td></tr>")[0]);
    }
    var self=this;
    $(tbody).find(".clickable-row").click(function(event) {
        
        $(self.selectOpDialog).modal("hide");

        var id=$(this).data("id")
        self.addOp(getElementByKey(self.searchedOps,"id",id));
        $.ajax({
            type:"GET",
            async:false,
            dataType:"json",
            url: restApiUrl+"algparams/?strategies="+id,
            success: function(data){
                for(var i=0;i<data.length;++i)self.addParam(data[i]);
            }
        });
    });
}

TemplAlgCreator.prototype.findParamsSelectParamDialog=function(str){
    var self=this;
    this.searchedParams=[];
    $.ajax({
        type:"GET",
        async:false,
        dataType:"json",
        url: restApiUrl+"algparams/"+(str.length>0 ? ("?name="+str) : ""),
        success: function(data){
            self.searchedParams=data;
        }
    });
    this.clearSearchedParamDialogTable();
    var tbody=this.selectParamDialogTable.getElementsByTagName("tbody")[0];
    for(var i=0;i<this.searchedParams.length;++i){
        tbody.appendChild($("<tr class='clickable-row' data-id='"+this.searchedParams[i].id+"'> <td>"+this.searchedParams[i].id+"</td><td>"+intTypeToString(this.searchedParams[i].type)+"</td><td>"+this.searchedParams[i].name+"</td></tr>")[0]);
    }
    var self=this;
    $(tbody).find(".clickable-row").click(function(event) {
        $(self.selectParamDialog).modal("hide");
        self.addParam(getElementByKey(self.searchedParams,"id",$(this).data("id")));
    });
}


TemplAlgCreator.prototype.addOp=function(op){
    this.operators.push(op);
    if(this.selectedOpTable.style.display=="none")this.selectedOpTable.style.display="";
    var elem=$("<tr data-id='"+op.id+"'> <td>"+op.id+" <input type='hidden' name='op_"+op.id+"' value='"+op.id+"'/></td><td>"+op.name+"</td><td width='30px' class='text-center'><span class='glyphicon glyphicon-remove' style='cursor:pointer;' aria-hidden='true'></span></td></tr>");
    var self=this;
    elem.find("span").click(function(event){
        var tt=$(this).closest("tr").data("id");
        self.removeOp($(this).closest("tr").data("id"));
    });
    this.selectedOpTable.getElementsByTagName("tbody")[0].appendChild(elem[0]);
}

TemplAlgCreator.prototype.addParam=function(op){
    this.params.push(op);
    if(this.selectedParamTable.style.display=="none") this.selectedParamTable.style.display="";
    var elem=$("<tr data-id='"+op.id+"'> <td>"+op.id+" <input type='hidden' name='param_"+op.id+"' value='"+op.id+"'/></td><td>"+intTypeToString(op.type)+"</td><td>"+op.name+"</td><td width='30px' class='text-center'><span class='glyphicon glyphicon-remove' style='cursor:pointer;' aria-hidden='true'></span></td></tr>");
    var self=this;
    elem.find("span").click(function(event){
        var tt=$(this).closest("tr").data("id");
        self.removeParam($(this).closest("tr").data("id"));
    });
    this.selectedParamTable.getElementsByTagName("tbody")[0].appendChild(elem[0]);
}


TemplAlgCreator.prototype.removeOp=function(opId){
    for(var i=0;i<this.operators.length;++i){
        if(this.operators[i].id=opId){
            this.operators.splice(i,1);
            break;
        }
    }
    $(this.selectedOpTable).find("[data-id="+opId+"]").remove();
    if(this.operators.length==0)this.selectedOpTable.style.display="none";
}

TemplAlgCreator.prototype.removeParam=function(id){
    for(var i=0;i<this.params.length;++i){
        if(this.params[i].id=id){
            this.params.splice(i,1);
            break;
        }
    }
    $(this.selectedParamTable).find("[data-id="+id+"]").remove();
    if(this.params.length==0)this.selectedParamTable.style.display="none";
}