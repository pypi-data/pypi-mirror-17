﻿/*
 Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
CKEDITOR.dialog.add("smiley",function(f){for(var e=f.config,a=f.lang.smiley,h=e.smiley_images,g=e.smiley_columns||8,k,m=function(l){var c=l.data.getTarget(),b=c.getName();if("a"==b)c=c.getChild(0);else if("img"!=b)return;var b=c.getAttribute("cke_src"),a=c.getAttribute("title"),c=f.document.createElement("img",{attributes:{src:b,"data-cke-saved-src":b,title:a,alt:a,width:c.$.width,height:c.$.height}});f.insertElement(c);k.hide();l.data.preventDefault()},q=CKEDITOR.tools.addFunction(function(a,c){a=
new CKEDITOR.dom.event(a);c=new CKEDITOR.dom.element(c);var b;b=a.getKeystroke();var d="rtl"==f.lang.dir;switch(b){case 38:if(b=c.getParent().getParent().getPrevious())b=b.getChild([c.getParent().getIndex(),0]),b.focus();a.preventDefault();break;case 40:(b=c.getParent().getParent().getNext())&&(b=b.getChild([c.getParent().getIndex(),0]))&&b.focus();a.preventDefault();break;case 32:m({data:a});a.preventDefault();break;case d?37:39:if(b=c.getParent().getNext())b=b.getChild(0),b.focus(),a.preventDefault(!0);
else if(b=c.getParent().getParent().getNext())(b=b.getChild([0,0]))&&b.focus(),a.preventDefault(!0);break;case d?39:37:if(b=c.getParent().getPrevious())b=b.getChild(0),b.focus(),a.preventDefault(!0);else if(b=c.getParent().getParent().getPrevious())b=b.getLast().getChild(0),b.focus(),a.preventDefault(!0)}}),d=CKEDITOR.tools.getNextId()+"_smiley_emtions_label",d=['\x3cdiv\x3e\x3cspan id\x3d"'+d+'" class\x3d"cke_voice_label"\x3e'+a.options+"\x3c/span\x3e",'\x3ctable role\x3d"listbox" aria-labelledby\x3d"'+
d+'" style\x3d"width:100%;height:100%;border-collapse:separate;" cellspacing\x3d"2" cellpadding\x3d"2"',CKEDITOR.env.ie&&CKEDITOR.env.quirks?' style\x3d"position:absolute;"':"","\x3e\x3ctbody\x3e"],n=h.length,a=0;a<n;a++){0===a%g&&d.push('\x3ctr role\x3d"presentation"\x3e');var p="cke_smile_label_"+a+"_"+CKEDITOR.tools.getNextNumber();d.push('\x3ctd class\x3d"cke_dark_background cke_centered" style\x3d"vertical-align: middle;" role\x3d"presentation"\x3e\x3ca href\x3d"javascript:void(0)" role\x3d"option"',
' aria-posinset\x3d"'+(a+1)+'"',' aria-setsize\x3d"'+n+'"',' aria-labelledby\x3d"'+p+'"',' class\x3d"cke_smile cke_hand" tabindex\x3d"-1" onkeydown\x3d"CKEDITOR.tools.callFunction( ',q,', event, this );"\x3e','\x3cimg class\x3d"cke_hand" title\x3d"',e.smiley_descriptions[a],'" cke_src\x3d"',CKEDITOR.tools.htmlEncode(e.smiley_path+h[a]),'" alt\x3d"',e.smiley_descriptions[a],'"',' src\x3d"',CKEDITOR.tools.htmlEncode(e.smiley_path+h[a]),'"',CKEDITOR.env.ie?" onload\x3d\"this.setAttribute('width', 2); this.removeAttribute('width');\" ":
"",'\x3e\x3cspan id\x3d"'+p+'" class\x3d"cke_voice_label"\x3e'+e.smiley_descriptions[a]+"\x3c/span\x3e\x3c/a\x3e","\x3c/td\x3e");a%g==g-1&&d.push("\x3c/tr\x3e")}if(a<g-1){for(;a<g-1;a++)d.push("\x3ctd\x3e\x3c/td\x3e");d.push("\x3c/tr\x3e")}d.push("\x3c/tbody\x3e\x3c/table\x3e\x3c/div\x3e");e={type:"html",id:"smileySelector",html:d.join(""),onLoad:function(a){k=a.sender},focus:function(){var a=this;setTimeout(function(){a.getElement().getElementsByTag("a").getItem(0).focus()},0)},onClick:m,style:"width: 100%; border-collapse: separate;"};
return{title:f.lang.smiley.title,minWidth:270,minHeight:120,contents:[{id:"tab1",label:"",title:"",expand:!0,padding:0,elements:[e]}],buttons:[CKEDITOR.dialog.cancelButton]}});