"use strict";(self.webpackChunkreact_admin_upgrade=self.webpackChunkreact_admin_upgrade||[]).push([[9214],{79214:function(e,n,t){t.r(n),t.d(n,{CompletionAdapter:function(){return pn},DefinitionAdapter:function(){return In},DiagnosticsAdapter:function(){return hn},DocumentColorAdapter:function(){return jn},DocumentFormattingEditProvider:function(){return Ln},DocumentHighlightAdapter:function(){return xn},DocumentLinkAdapter:function(){return Pn},DocumentRangeFormattingEditProvider:function(){return Fn},DocumentSymbolAdapter:function(){return Dn},FoldingRangeAdapter:function(){return On},HoverAdapter:function(){return bn},ReferenceAdapter:function(){return Rn},RenameAdapter:function(){return Tn},SelectionRangeAdapter:function(){return Nn},WorkerManager:function(){return ge},fromPosition:function(){return mn},fromRange:function(){return _n},setupMode:function(){return Un},toRange:function(){return kn},toTextEdit:function(){return yn}});var r,i,o=t(15671),a=t(43144),s=t(4942),u=t(37762),c=t(94389),d=Object.defineProperty,g=Object.getOwnPropertyDescriptor,f=Object.getOwnPropertyNames,l=Object.prototype.hasOwnProperty,h=function(e,n,t,r){if(n&&"object"===typeof n||"function"===typeof n){var i,o=(0,u.Z)(f(n));try{var a=function(){var o=i.value;l.call(e,o)||o===t||d(e,o,{get:function(){return n[o]},enumerable:!(r=g(n,o))||r.enumerable})};for(o.s();!(i=o.n()).done;)a()}catch(s){o.e(s)}finally{o.f()}}return e},v={};h(v,r=c,"default"),i&&h(i,r,"default");var p,m,_,k,w,y,b,E,C,x,A,I,S,R,T,D,M,P,L,F,Z,j,O,N,U,W,V,H,K,z,X,B,$,q,Q,G,J,Y,ee,ne,te,re,ie,oe,ae,se,ue,ce,de,ge=function(){function e(n){var t=this;(0,o.Z)(this,e),(0,s.Z)(this,"_defaults",void 0),(0,s.Z)(this,"_idleCheckInterval",void 0),(0,s.Z)(this,"_lastUsedTime",void 0),(0,s.Z)(this,"_configChangeListener",void 0),(0,s.Z)(this,"_worker",void 0),(0,s.Z)(this,"_client",void 0),this._defaults=n,this._worker=null,this._client=null,this._idleCheckInterval=window.setInterval((function(){return t._checkIfIdle()}),3e4),this._lastUsedTime=0,this._configChangeListener=this._defaults.onDidChange((function(){return t._stopWorker()}))}return(0,a.Z)(e,[{key:"_stopWorker",value:function(){this._worker&&(this._worker.dispose(),this._worker=null),this._client=null}},{key:"dispose",value:function(){clearInterval(this._idleCheckInterval),this._configChangeListener.dispose(),this._stopWorker()}},{key:"_checkIfIdle",value:function(){this._worker&&(Date.now()-this._lastUsedTime>12e4&&this._stopWorker())}},{key:"_getClient",value:function(){return this._lastUsedTime=Date.now(),this._client||(this._worker=v.editor.createWebWorker({moduleId:"vs/language/css/cssWorker",label:this._defaults.languageId,createData:{options:this._defaults.options,languageId:this._defaults.languageId}}),this._client=this._worker.getProxy()),this._client}},{key:"getLanguageServiceWorker",value:function(){for(var e,n=this,t=arguments.length,r=new Array(t),i=0;i<t;i++)r[i]=arguments[i];return this._getClient().then((function(n){e=n})).then((function(e){if(n._worker)return n._worker.withSyncedResources(r)})).then((function(n){return e}))}}]),e}();(m=p||(p={})).MIN_VALUE=-2147483648,m.MAX_VALUE=2147483647,(k=_||(_={})).MIN_VALUE=0,k.MAX_VALUE=2147483647,(y=w||(w={})).create=function(e,n){return e===Number.MAX_VALUE&&(e=_.MAX_VALUE),n===Number.MAX_VALUE&&(n=_.MAX_VALUE),{line:e,character:n}},y.is=function(e){var n=e;return fn.objectLiteral(n)&&fn.uinteger(n.line)&&fn.uinteger(n.character)},(E=b||(b={})).create=function(e,n,t,r){if(fn.uinteger(e)&&fn.uinteger(n)&&fn.uinteger(t)&&fn.uinteger(r))return{start:w.create(e,n),end:w.create(t,r)};if(w.is(e)&&w.is(n))return{start:e,end:n};throw new Error("Range#create called with invalid arguments["+e+", "+n+", "+t+", "+r+"]")},E.is=function(e){var n=e;return fn.objectLiteral(n)&&w.is(n.start)&&w.is(n.end)},(x=C||(C={})).create=function(e,n){return{uri:e,range:n}},x.is=function(e){var n=e;return fn.defined(n)&&b.is(n.range)&&(fn.string(n.uri)||fn.undefined(n.uri))},(I=A||(A={})).create=function(e,n,t,r){return{targetUri:e,targetRange:n,targetSelectionRange:t,originSelectionRange:r}},I.is=function(e){var n=e;return fn.defined(n)&&b.is(n.targetRange)&&fn.string(n.targetUri)&&(b.is(n.targetSelectionRange)||fn.undefined(n.targetSelectionRange))&&(b.is(n.originSelectionRange)||fn.undefined(n.originSelectionRange))},(R=S||(S={})).create=function(e,n,t,r){return{red:e,green:n,blue:t,alpha:r}},R.is=function(e){var n=e;return fn.numberRange(n.red,0,1)&&fn.numberRange(n.green,0,1)&&fn.numberRange(n.blue,0,1)&&fn.numberRange(n.alpha,0,1)},(D=T||(T={})).create=function(e,n){return{range:e,color:n}},D.is=function(e){var n=e;return b.is(n.range)&&S.is(n.color)},(P=M||(M={})).create=function(e,n,t){return{label:e,textEdit:n,additionalTextEdits:t}},P.is=function(e){var n=e;return fn.string(n.label)&&(fn.undefined(n.textEdit)||q.is(n))&&(fn.undefined(n.additionalTextEdits)||fn.typedArray(n.additionalTextEdits,q.is))},(F=L||(L={})).Comment="comment",F.Imports="imports",F.Region="region",(j=Z||(Z={})).create=function(e,n,t,r,i){var o={startLine:e,endLine:n};return fn.defined(t)&&(o.startCharacter=t),fn.defined(r)&&(o.endCharacter=r),fn.defined(i)&&(o.kind=i),o},j.is=function(e){var n=e;return fn.uinteger(n.startLine)&&fn.uinteger(n.startLine)&&(fn.undefined(n.startCharacter)||fn.uinteger(n.startCharacter))&&(fn.undefined(n.endCharacter)||fn.uinteger(n.endCharacter))&&(fn.undefined(n.kind)||fn.string(n.kind))},(N=O||(O={})).create=function(e,n){return{location:e,message:n}},N.is=function(e){var n=e;return fn.defined(n)&&C.is(n.location)&&fn.string(n.message)},(W=U||(U={})).Error=1,W.Warning=2,W.Information=3,W.Hint=4,(H=V||(V={})).Unnecessary=1,H.Deprecated=2,(K||(K={})).is=function(e){var n=e;return void 0!==n&&null!==n&&fn.string(n.href)},(X=z||(z={})).create=function(e,n,t,r,i,o){var a={range:e,message:n};return fn.defined(t)&&(a.severity=t),fn.defined(r)&&(a.code=r),fn.defined(i)&&(a.source=i),fn.defined(o)&&(a.relatedInformation=o),a},X.is=function(e){var n,t=e;return fn.defined(t)&&b.is(t.range)&&fn.string(t.message)&&(fn.number(t.severity)||fn.undefined(t.severity))&&(fn.integer(t.code)||fn.string(t.code)||fn.undefined(t.code))&&(fn.undefined(t.codeDescription)||fn.string(null===(n=t.codeDescription)||void 0===n?void 0:n.href))&&(fn.string(t.source)||fn.undefined(t.source))&&(fn.undefined(t.relatedInformation)||fn.typedArray(t.relatedInformation,O.is))},($=B||(B={})).create=function(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={title:e,command:n};return fn.defined(t)&&t.length>0&&(i.arguments=t),i},$.is=function(e){var n=e;return fn.defined(n)&&fn.string(n.title)&&fn.string(n.command)},(Q=q||(q={})).replace=function(e,n){return{range:e,newText:n}},Q.insert=function(e,n){return{range:{start:e,end:e},newText:n}},Q.del=function(e){return{range:e,newText:""}},Q.is=function(e){var n=e;return fn.objectLiteral(n)&&fn.string(n.newText)&&b.is(n.range)},(J=G||(G={})).create=function(e,n,t){var r={label:e};return void 0!==n&&(r.needsConfirmation=n),void 0!==t&&(r.description=t),r},J.is=function(e){var n=e;return void 0!==n&&fn.objectLiteral(n)&&fn.string(n.label)&&(fn.boolean(n.needsConfirmation)||void 0===n.needsConfirmation)&&(fn.string(n.description)||void 0===n.description)},(Y||(Y={})).is=function(e){return"string"===typeof e},(ne=ee||(ee={})).replace=function(e,n,t){return{range:e,newText:n,annotationId:t}},ne.insert=function(e,n,t){return{range:{start:e,end:e},newText:n,annotationId:t}},ne.del=function(e,n){return{range:e,newText:"",annotationId:n}},ne.is=function(e){var n=e;return q.is(n)&&(G.is(n.annotationId)||Y.is(n.annotationId))},(re=te||(te={})).create=function(e,n){return{textDocument:e,edits:n}},re.is=function(e){var n=e;return fn.defined(n)&&pe.is(n.textDocument)&&Array.isArray(n.edits)},(oe=ie||(ie={})).create=function(e,n,t){var r={kind:"create",uri:e};return void 0===n||void 0===n.overwrite&&void 0===n.ignoreIfExists||(r.options=n),void 0!==t&&(r.annotationId=t),r},oe.is=function(e){var n=e;return n&&"create"===n.kind&&fn.string(n.uri)&&(void 0===n.options||(void 0===n.options.overwrite||fn.boolean(n.options.overwrite))&&(void 0===n.options.ignoreIfExists||fn.boolean(n.options.ignoreIfExists)))&&(void 0===n.annotationId||Y.is(n.annotationId))},(se=ae||(ae={})).create=function(e,n,t,r){var i={kind:"rename",oldUri:e,newUri:n};return void 0===t||void 0===t.overwrite&&void 0===t.ignoreIfExists||(i.options=t),void 0!==r&&(i.annotationId=r),i},se.is=function(e){var n=e;return n&&"rename"===n.kind&&fn.string(n.oldUri)&&fn.string(n.newUri)&&(void 0===n.options||(void 0===n.options.overwrite||fn.boolean(n.options.overwrite))&&(void 0===n.options.ignoreIfExists||fn.boolean(n.options.ignoreIfExists)))&&(void 0===n.annotationId||Y.is(n.annotationId))},(ce=ue||(ue={})).create=function(e,n,t){var r={kind:"delete",uri:e};return void 0===n||void 0===n.recursive&&void 0===n.ignoreIfNotExists||(r.options=n),void 0!==t&&(r.annotationId=t),r},ce.is=function(e){var n=e;return n&&"delete"===n.kind&&fn.string(n.uri)&&(void 0===n.options||(void 0===n.options.recursive||fn.boolean(n.options.recursive))&&(void 0===n.options.ignoreIfNotExists||fn.boolean(n.options.ignoreIfNotExists)))&&(void 0===n.annotationId||Y.is(n.annotationId))},(de||(de={})).is=function(e){var n=e;return n&&(void 0!==n.changes||void 0!==n.documentChanges)&&(void 0===n.documentChanges||n.documentChanges.every((function(e){return fn.string(e.kind)?ie.is(e)||ae.is(e)||ue.is(e):te.is(e)})))};var fe,le,he,ve,pe,me,_e,ke,we,ye,be,Ee,Ce,xe,Ae,Ie,Se,Re,Te,De,Me,Pe,Le,Fe,Ze,je,Oe,Ne,Ue,We,Ve,He,Ke,ze,Xe,Be,$e,qe,Qe,Ge,Je,Ye,en,nn,tn,rn,on,an,sn,un,cn,dn=function(){function e(e,n){this.edits=e,this.changeAnnotations=n}return e.prototype.insert=function(e,n,t){var r,i;if(void 0===t?r=q.insert(e,n):Y.is(t)?(i=t,r=ee.insert(e,n,t)):(this.assertChangeAnnotations(this.changeAnnotations),i=this.changeAnnotations.manage(t),r=ee.insert(e,n,i)),this.edits.push(r),void 0!==i)return i},e.prototype.replace=function(e,n,t){var r,i;if(void 0===t?r=q.replace(e,n):Y.is(t)?(i=t,r=ee.replace(e,n,t)):(this.assertChangeAnnotations(this.changeAnnotations),i=this.changeAnnotations.manage(t),r=ee.replace(e,n,i)),this.edits.push(r),void 0!==i)return i},e.prototype.delete=function(e,n){var t,r;if(void 0===n?t=q.del(e):Y.is(n)?(r=n,t=ee.del(e,n)):(this.assertChangeAnnotations(this.changeAnnotations),r=this.changeAnnotations.manage(n),t=ee.del(e,r)),this.edits.push(t),void 0!==r)return r},e.prototype.add=function(e){this.edits.push(e)},e.prototype.all=function(){return this.edits},e.prototype.clear=function(){this.edits.splice(0,this.edits.length)},e.prototype.assertChangeAnnotations=function(e){if(void 0===e)throw new Error("Text edit change is not configured to manage change annotations.")},e}(),gn=function(){function e(e){this._annotations=void 0===e?Object.create(null):e,this._counter=0,this._size=0}return e.prototype.all=function(){return this._annotations},Object.defineProperty(e.prototype,"size",{get:function(){return this._size},enumerable:!1,configurable:!0}),e.prototype.manage=function(e,n){var t;if(Y.is(e)?t=e:(t=this.nextId(),n=e),void 0!==this._annotations[t])throw new Error("Id "+t+" is already in use.");if(void 0===n)throw new Error("No annotation provided for id "+t);return this._annotations[t]=n,this._size++,t},e.prototype.nextId=function(){return this._counter++,this._counter.toString()},e}();!function(){function e(e){var n=this;this._textEditChanges=Object.create(null),void 0!==e?(this._workspaceEdit=e,e.documentChanges?(this._changeAnnotations=new gn(e.changeAnnotations),e.changeAnnotations=this._changeAnnotations.all(),e.documentChanges.forEach((function(e){if(te.is(e)){var t=new dn(e.edits,n._changeAnnotations);n._textEditChanges[e.textDocument.uri]=t}}))):e.changes&&Object.keys(e.changes).forEach((function(t){var r=new dn(e.changes[t]);n._textEditChanges[t]=r}))):this._workspaceEdit={}}Object.defineProperty(e.prototype,"edit",{get:function(){return this.initDocumentChanges(),void 0!==this._changeAnnotations&&(0===this._changeAnnotations.size?this._workspaceEdit.changeAnnotations=void 0:this._workspaceEdit.changeAnnotations=this._changeAnnotations.all()),this._workspaceEdit},enumerable:!1,configurable:!0}),e.prototype.getTextEditChange=function(e){if(pe.is(e)){if(this.initDocumentChanges(),void 0===this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for document changes.");var n={uri:e.uri,version:e.version};if(!(r=this._textEditChanges[n.uri])){var t={textDocument:n,edits:i=[]};this._workspaceEdit.documentChanges.push(t),r=new dn(i,this._changeAnnotations),this._textEditChanges[n.uri]=r}return r}if(this.initChanges(),void 0===this._workspaceEdit.changes)throw new Error("Workspace edit is not configured for normal text edit changes.");var r;if(!(r=this._textEditChanges[e])){var i=[];this._workspaceEdit.changes[e]=i,r=new dn(i),this._textEditChanges[e]=r}return r},e.prototype.initDocumentChanges=function(){void 0===this._workspaceEdit.documentChanges&&void 0===this._workspaceEdit.changes&&(this._changeAnnotations=new gn,this._workspaceEdit.documentChanges=[],this._workspaceEdit.changeAnnotations=this._changeAnnotations.all())},e.prototype.initChanges=function(){void 0===this._workspaceEdit.documentChanges&&void 0===this._workspaceEdit.changes&&(this._workspaceEdit.changes=Object.create(null))},e.prototype.createFile=function(e,n,t){if(this.initDocumentChanges(),void 0===this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for document changes.");var r,i,o;if(G.is(n)||Y.is(n)?r=n:t=n,void 0===r?i=ie.create(e,t):(o=Y.is(r)?r:this._changeAnnotations.manage(r),i=ie.create(e,t,o)),this._workspaceEdit.documentChanges.push(i),void 0!==o)return o},e.prototype.renameFile=function(e,n,t,r){if(this.initDocumentChanges(),void 0===this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for document changes.");var i,o,a;if(G.is(t)||Y.is(t)?i=t:r=t,void 0===i?o=ae.create(e,n,r):(a=Y.is(i)?i:this._changeAnnotations.manage(i),o=ae.create(e,n,r,a)),this._workspaceEdit.documentChanges.push(o),void 0!==a)return a},e.prototype.deleteFile=function(e,n,t){if(this.initDocumentChanges(),void 0===this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for document changes.");var r,i,o;if(G.is(n)||Y.is(n)?r=n:t=n,void 0===r?i=ue.create(e,t):(o=Y.is(r)?r:this._changeAnnotations.manage(r),i=ue.create(e,t,o)),this._workspaceEdit.documentChanges.push(i),void 0!==o)return o}}();(le=fe||(fe={})).create=function(e){return{uri:e}},le.is=function(e){var n=e;return fn.defined(n)&&fn.string(n.uri)},(ve=he||(he={})).create=function(e,n){return{uri:e,version:n}},ve.is=function(e){var n=e;return fn.defined(n)&&fn.string(n.uri)&&fn.integer(n.version)},(me=pe||(pe={})).create=function(e,n){return{uri:e,version:n}},me.is=function(e){var n=e;return fn.defined(n)&&fn.string(n.uri)&&(null===n.version||fn.integer(n.version))},(ke=_e||(_e={})).create=function(e,n,t,r){return{uri:e,languageId:n,version:t,text:r}},ke.is=function(e){var n=e;return fn.defined(n)&&fn.string(n.uri)&&fn.string(n.languageId)&&fn.integer(n.version)&&fn.string(n.text)},(ye=we||(we={})).PlainText="plaintext",ye.Markdown="markdown",function(e){e.is=function(n){var t=n;return t===e.PlainText||t===e.Markdown}}(we||(we={})),(be||(be={})).is=function(e){var n=e;return fn.objectLiteral(e)&&we.is(n.kind)&&fn.string(n.value)},(Ce=Ee||(Ee={})).Text=1,Ce.Method=2,Ce.Function=3,Ce.Constructor=4,Ce.Field=5,Ce.Variable=6,Ce.Class=7,Ce.Interface=8,Ce.Module=9,Ce.Property=10,Ce.Unit=11,Ce.Value=12,Ce.Enum=13,Ce.Keyword=14,Ce.Snippet=15,Ce.Color=16,Ce.File=17,Ce.Reference=18,Ce.Folder=19,Ce.EnumMember=20,Ce.Constant=21,Ce.Struct=22,Ce.Event=23,Ce.Operator=24,Ce.TypeParameter=25,(Ae=xe||(xe={})).PlainText=1,Ae.Snippet=2,(Ie||(Ie={})).Deprecated=1,(Re=Se||(Se={})).create=function(e,n,t){return{newText:e,insert:n,replace:t}},Re.is=function(e){var n=e;return n&&fn.string(n.newText)&&b.is(n.insert)&&b.is(n.replace)},(De=Te||(Te={})).asIs=1,De.adjustIndentation=2,(Me||(Me={})).create=function(e){return{label:e}},(Pe||(Pe={})).create=function(e,n){return{items:e||[],isIncomplete:!!n}},(Fe=Le||(Le={})).fromPlainText=function(e){return e.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")},Fe.is=function(e){var n=e;return fn.string(n)||fn.objectLiteral(n)&&fn.string(n.language)&&fn.string(n.value)},(Ze||(Ze={})).is=function(e){var n=e;return!!n&&fn.objectLiteral(n)&&(be.is(n.contents)||Le.is(n.contents)||fn.typedArray(n.contents,Le.is))&&(void 0===e.range||b.is(e.range))},(je||(je={})).create=function(e,n){return n?{label:e,documentation:n}:{label:e}},(Oe||(Oe={})).create=function(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={label:e};return fn.defined(n)&&(i.documentation=n),fn.defined(t)?i.parameters=t:i.parameters=[],i},(Ue=Ne||(Ne={})).Text=1,Ue.Read=2,Ue.Write=3,(We||(We={})).create=function(e,n){var t={range:e};return fn.number(n)&&(t.kind=n),t},(He=Ve||(Ve={})).File=1,He.Module=2,He.Namespace=3,He.Package=4,He.Class=5,He.Method=6,He.Property=7,He.Field=8,He.Constructor=9,He.Enum=10,He.Interface=11,He.Function=12,He.Variable=13,He.Constant=14,He.String=15,He.Number=16,He.Boolean=17,He.Array=18,He.Object=19,He.Key=20,He.Null=21,He.EnumMember=22,He.Struct=23,He.Event=24,He.Operator=25,He.TypeParameter=26,(Ke||(Ke={})).Deprecated=1,(ze||(ze={})).create=function(e,n,t,r,i){var o={name:e,kind:n,location:{uri:r,range:t}};return i&&(o.containerName=i),o},(Be=Xe||(Xe={})).create=function(e,n,t,r,i,o){var a={name:e,detail:n,kind:t,range:r,selectionRange:i};return void 0!==o&&(a.children=o),a},Be.is=function(e){var n=e;return n&&fn.string(n.name)&&fn.number(n.kind)&&b.is(n.range)&&b.is(n.selectionRange)&&(void 0===n.detail||fn.string(n.detail))&&(void 0===n.deprecated||fn.boolean(n.deprecated))&&(void 0===n.children||Array.isArray(n.children))&&(void 0===n.tags||Array.isArray(n.tags))},(qe=$e||($e={})).Empty="",qe.QuickFix="quickfix",qe.Refactor="refactor",qe.RefactorExtract="refactor.extract",qe.RefactorInline="refactor.inline",qe.RefactorRewrite="refactor.rewrite",qe.Source="source",qe.SourceOrganizeImports="source.organizeImports",qe.SourceFixAll="source.fixAll",(Ge=Qe||(Qe={})).create=function(e,n){var t={diagnostics:e};return void 0!==n&&null!==n&&(t.only=n),t},Ge.is=function(e){var n=e;return fn.defined(n)&&fn.typedArray(n.diagnostics,z.is)&&(void 0===n.only||fn.typedArray(n.only,fn.string))},(Ye=Je||(Je={})).create=function(e,n,t){var r={title:e},i=!0;return"string"===typeof n?(i=!1,r.kind=n):B.is(n)?r.command=n:r.edit=n,i&&void 0!==t&&(r.kind=t),r},Ye.is=function(e){var n=e;return n&&fn.string(n.title)&&(void 0===n.diagnostics||fn.typedArray(n.diagnostics,z.is))&&(void 0===n.kind||fn.string(n.kind))&&(void 0!==n.edit||void 0!==n.command)&&(void 0===n.command||B.is(n.command))&&(void 0===n.isPreferred||fn.boolean(n.isPreferred))&&(void 0===n.edit||de.is(n.edit))},(nn=en||(en={})).create=function(e,n){var t={range:e};return fn.defined(n)&&(t.data=n),t},nn.is=function(e){var n=e;return fn.defined(n)&&b.is(n.range)&&(fn.undefined(n.command)||B.is(n.command))},(rn=tn||(tn={})).create=function(e,n){return{tabSize:e,insertSpaces:n}},rn.is=function(e){var n=e;return fn.defined(n)&&fn.uinteger(n.tabSize)&&fn.boolean(n.insertSpaces)},(an=on||(on={})).create=function(e,n,t){return{range:e,target:n,data:t}},an.is=function(e){var n=e;return fn.defined(n)&&b.is(n.range)&&(fn.undefined(n.target)||fn.string(n.target))},(un=sn||(sn={})).create=function(e,n){return{range:e,parent:n}},un.is=function(e){var n=e;return void 0!==n&&b.is(n.range)&&(void 0===n.parent||un.is(n.parent))},function(e){function n(e,t){if(e.length<=1)return e;var r=e.length/2|0,i=e.slice(0,r),o=e.slice(r);n(i,t),n(o,t);for(var a=0,s=0,u=0;a<i.length&&s<o.length;){var c=t(i[a],o[s]);e[u++]=c<=0?i[a++]:o[s++]}for(;a<i.length;)e[u++]=i[a++];for(;s<o.length;)e[u++]=o[s++];return e}e.create=function(e,n,t,r){return new ln(e,n,t,r)},e.is=function(e){var n=e;return!!(fn.defined(n)&&fn.string(n.uri)&&(fn.undefined(n.languageId)||fn.string(n.languageId))&&fn.uinteger(n.lineCount)&&fn.func(n.getText)&&fn.func(n.positionAt)&&fn.func(n.offsetAt))},e.applyEdits=function(e,t){for(var r=e.getText(),i=n(t,(function(e,n){var t=e.range.start.line-n.range.start.line;return 0===t?e.range.start.character-n.range.start.character:t})),o=r.length,a=i.length-1;a>=0;a--){var s=i[a],u=e.offsetAt(s.range.start),c=e.offsetAt(s.range.end);if(!(c<=o))throw new Error("Overlapping edit");r=r.substring(0,u)+s.newText+r.substring(c,r.length),o=u}return r}}(cn||(cn={}));var fn,ln=function(){function e(e,n,t,r){this._uri=e,this._languageId=n,this._version=t,this._content=r,this._lineOffsets=void 0}return Object.defineProperty(e.prototype,"uri",{get:function(){return this._uri},enumerable:!1,configurable:!0}),Object.defineProperty(e.prototype,"languageId",{get:function(){return this._languageId},enumerable:!1,configurable:!0}),Object.defineProperty(e.prototype,"version",{get:function(){return this._version},enumerable:!1,configurable:!0}),e.prototype.getText=function(e){if(e){var n=this.offsetAt(e.start),t=this.offsetAt(e.end);return this._content.substring(n,t)}return this._content},e.prototype.update=function(e,n){this._content=e.text,this._version=n,this._lineOffsets=void 0},e.prototype.getLineOffsets=function(){if(void 0===this._lineOffsets){for(var e=[],n=this._content,t=!0,r=0;r<n.length;r++){t&&(e.push(r),t=!1);var i=n.charAt(r);t="\r"===i||"\n"===i,"\r"===i&&r+1<n.length&&"\n"===n.charAt(r+1)&&r++}t&&n.length>0&&e.push(n.length),this._lineOffsets=e}return this._lineOffsets},e.prototype.positionAt=function(e){e=Math.max(Math.min(e,this._content.length),0);var n=this.getLineOffsets(),t=0,r=n.length;if(0===r)return w.create(0,e);for(;t<r;){var i=Math.floor((t+r)/2);n[i]>e?r=i:t=i+1}var o=t-1;return w.create(o,e-n[o])},e.prototype.offsetAt=function(e){var n=this.getLineOffsets();if(e.line>=n.length)return this._content.length;if(e.line<0)return 0;var t=n[e.line],r=e.line+1<n.length?n[e.line+1]:this._content.length;return Math.max(Math.min(t+e.character,r),t)},Object.defineProperty(e.prototype,"lineCount",{get:function(){return this.getLineOffsets().length},enumerable:!1,configurable:!0}),e}();!function(e){var n=Object.prototype.toString;e.defined=function(e){return"undefined"!==typeof e},e.undefined=function(e){return"undefined"===typeof e},e.boolean=function(e){return!0===e||!1===e},e.string=function(e){return"[object String]"===n.call(e)},e.number=function(e){return"[object Number]"===n.call(e)},e.numberRange=function(e,t,r){return"[object Number]"===n.call(e)&&t<=e&&e<=r},e.integer=function(e){return"[object Number]"===n.call(e)&&-2147483648<=e&&e<=2147483647},e.uinteger=function(e){return"[object Number]"===n.call(e)&&0<=e&&e<=2147483647},e.func=function(e){return"[object Function]"===n.call(e)},e.objectLiteral=function(e){return null!==e&&"object"===typeof e},e.typedArray=function(e,n){return Array.isArray(e)&&e.every(n)}}(fn||(fn={}));var hn=function(){function e(n,t,r){var i=this;(0,o.Z)(this,e),(0,s.Z)(this,"_disposables",[]),(0,s.Z)(this,"_listener",Object.create(null)),this._languageId=n,this._worker=t;var a=function(e){var n,t=e.getLanguageId();t===i._languageId&&(i._listener[e.uri.toString()]=e.onDidChangeContent((function(){window.clearTimeout(n),n=window.setTimeout((function(){return i._doValidate(e.uri,t)}),500)})),i._doValidate(e.uri,t))},u=function(e){v.editor.setModelMarkers(e,i._languageId,[]);var n=e.uri.toString(),t=i._listener[n];t&&(t.dispose(),delete i._listener[n])};this._disposables.push(v.editor.onDidCreateModel(a)),this._disposables.push(v.editor.onWillDisposeModel(u)),this._disposables.push(v.editor.onDidChangeModelLanguage((function(e){u(e.model),a(e.model)}))),this._disposables.push(r((function(e){v.editor.getModels().forEach((function(e){e.getLanguageId()===i._languageId&&(u(e),a(e))}))}))),this._disposables.push({dispose:function(){for(var e in v.editor.getModels().forEach(u),i._listener)i._listener[e].dispose()}}),v.editor.getModels().forEach(a)}return(0,a.Z)(e,[{key:"dispose",value:function(){this._disposables.forEach((function(e){return e&&e.dispose()})),this._disposables.length=0}},{key:"_doValidate",value:function(e,n){this._worker(e).then((function(n){return n.doValidation(e.toString())})).then((function(t){var r=t.map((function(e){return function(e,n){var t="number"===typeof n.code?String(n.code):n.code;return{severity:vn(n.severity),startLineNumber:n.range.start.line+1,startColumn:n.range.start.character+1,endLineNumber:n.range.end.line+1,endColumn:n.range.end.character+1,message:n.message,code:t,source:n.source}}(0,e)})),i=v.editor.getModel(e);i&&i.getLanguageId()===n&&v.editor.setModelMarkers(i,n,r)})).then(void 0,(function(e){console.error(e)}))}}]),e}();function vn(e){switch(e){case U.Error:return v.MarkerSeverity.Error;case U.Warning:return v.MarkerSeverity.Warning;case U.Information:return v.MarkerSeverity.Info;case U.Hint:return v.MarkerSeverity.Hint;default:return v.MarkerSeverity.Info}}var pn=function(){function e(n,t){(0,o.Z)(this,e),this._worker=n,this._triggerCharacters=t}return(0,a.Z)(e,[{key:"triggerCharacters",get:function(){return this._triggerCharacters}},{key:"provideCompletionItems",value:function(e,n,t,r){var i=e.uri;return this._worker(i).then((function(e){return e.doComplete(i.toString(),mn(n))})).then((function(t){if(t){var r=e.getWordUntilPosition(n),i=new v.Range(n.lineNumber,r.startColumn,n.lineNumber,r.endColumn),o=t.items.map((function(e){var n,t,r={label:e.label,insertText:e.insertText||e.label,sortText:e.sortText,filterText:e.filterText,documentation:e.documentation,detail:e.detail,command:(n=e.command,n&&"editor.action.triggerSuggest"===n.command?{id:n.command,title:n.title,arguments:n.arguments}:void 0),range:i,kind:wn(e.kind)};return e.textEdit&&("undefined"!==typeof(t=e.textEdit).insert&&"undefined"!==typeof t.replace?r.range={insert:kn(e.textEdit.insert),replace:kn(e.textEdit.replace)}:r.range=kn(e.textEdit.range),r.insertText=e.textEdit.newText),e.additionalTextEdits&&(r.additionalTextEdits=e.additionalTextEdits.map(yn)),e.insertTextFormat===xe.Snippet&&(r.insertTextRules=v.languages.CompletionItemInsertTextRule.InsertAsSnippet),r}));return{isIncomplete:t.isIncomplete,suggestions:o}}}))}}]),e}();function mn(e){if(e)return{character:e.column-1,line:e.lineNumber-1}}function _n(e){if(e)return{start:{line:e.startLineNumber-1,character:e.startColumn-1},end:{line:e.endLineNumber-1,character:e.endColumn-1}}}function kn(e){if(e)return new v.Range(e.start.line+1,e.start.character+1,e.end.line+1,e.end.character+1)}function wn(e){var n=v.languages.CompletionItemKind;switch(e){case Ee.Text:return n.Text;case Ee.Method:return n.Method;case Ee.Function:return n.Function;case Ee.Constructor:return n.Constructor;case Ee.Field:return n.Field;case Ee.Variable:return n.Variable;case Ee.Class:return n.Class;case Ee.Interface:return n.Interface;case Ee.Module:return n.Module;case Ee.Property:return n.Property;case Ee.Unit:return n.Unit;case Ee.Value:return n.Value;case Ee.Enum:return n.Enum;case Ee.Keyword:return n.Keyword;case Ee.Snippet:return n.Snippet;case Ee.Color:return n.Color;case Ee.File:return n.File;case Ee.Reference:return n.Reference}return n.Property}function yn(e){if(e)return{range:kn(e.range),text:e.newText}}var bn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideHover",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.doHover(r.toString(),mn(n))})).then((function(e){if(e)return{range:kn(e.range),contents:Cn(e.contents)}}))}}]),e}();function En(e){return"string"===typeof e?{value:e}:(n=e)&&"object"===typeof n&&"string"===typeof n.kind?"plaintext"===e.kind?{value:e.value.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}:{value:e.value}:{value:"```"+e.language+"\n"+e.value+"\n```\n"};var n}function Cn(e){if(e)return Array.isArray(e)?e.map(En):[En(e)]}var xn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideDocumentHighlights",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.findDocumentHighlights(r.toString(),mn(n))})).then((function(e){if(e)return e.map((function(e){return{range:kn(e.range),kind:An(e.kind)}}))}))}}]),e}();function An(e){switch(e){case Ne.Read:return v.languages.DocumentHighlightKind.Read;case Ne.Write:return v.languages.DocumentHighlightKind.Write;case Ne.Text:return v.languages.DocumentHighlightKind.Text}return v.languages.DocumentHighlightKind.Text}var In=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideDefinition",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.findDefinition(r.toString(),mn(n))})).then((function(e){if(e)return[Sn(e)]}))}}]),e}();function Sn(e){return{uri:v.Uri.parse(e.uri),range:kn(e.range)}}var Rn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideReferences",value:function(e,n,t,r){var i=e.uri;return this._worker(i).then((function(e){return e.findReferences(i.toString(),mn(n))})).then((function(e){if(e)return e.map(Sn)}))}}]),e}(),Tn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideRenameEdits",value:function(e,n,t,r){var i=e.uri;return this._worker(i).then((function(e){return e.doRename(i.toString(),mn(n),t)})).then((function(e){return function(e){if(!e||!e.changes)return;var n=[];for(var t in e.changes){var r,i=v.Uri.parse(t),o=(0,u.Z)(e.changes[t]);try{for(o.s();!(r=o.n()).done;){var a=r.value;n.push({resource:i,versionId:void 0,textEdit:{range:kn(a.range),text:a.newText}})}}catch(s){o.e(s)}finally{o.f()}}return{edits:n}}(e)}))}}]),e}();var Dn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideDocumentSymbols",value:function(e,n){var t=e.uri;return this._worker(t).then((function(e){return e.findDocumentSymbols(t.toString())})).then((function(e){if(e)return e.map((function(e){return{name:e.name,detail:"",containerName:e.containerName,kind:Mn(e.kind),range:kn(e.location.range),selectionRange:kn(e.location.range),tags:[]}}))}))}}]),e}();function Mn(e){var n=v.languages.SymbolKind;switch(e){case Ve.File:return n.Array;case Ve.Module:return n.Module;case Ve.Namespace:return n.Namespace;case Ve.Package:return n.Package;case Ve.Class:return n.Class;case Ve.Method:return n.Method;case Ve.Property:return n.Property;case Ve.Field:return n.Field;case Ve.Constructor:return n.Constructor;case Ve.Enum:return n.Enum;case Ve.Interface:return n.Interface;case Ve.Function:return n.Function;case Ve.Variable:return n.Variable;case Ve.Constant:return n.Constant;case Ve.String:return n.String;case Ve.Number:return n.Number;case Ve.Boolean:return n.Boolean;case Ve.Array:return n.Array}return n.Function}var Pn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideLinks",value:function(e,n){var t=e.uri;return this._worker(t).then((function(e){return e.findDocumentLinks(t.toString())})).then((function(e){if(e)return{links:e.map((function(e){return{range:kn(e.range),url:e.target}}))}}))}}]),e}(),Ln=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideDocumentFormattingEdits",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.format(r.toString(),null,Zn(n)).then((function(e){if(e&&0!==e.length)return e.map(yn)}))}))}}]),e}(),Fn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideDocumentRangeFormattingEdits",value:function(e,n,t,r){var i=e.uri;return this._worker(i).then((function(e){return e.format(i.toString(),_n(n),Zn(t)).then((function(e){if(e&&0!==e.length)return e.map(yn)}))}))}}]),e}();function Zn(e){return{tabSize:e.tabSize,insertSpaces:e.insertSpaces}}var jn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideDocumentColors",value:function(e,n){var t=e.uri;return this._worker(t).then((function(e){return e.findDocumentColors(t.toString())})).then((function(e){if(e)return e.map((function(e){return{color:e.color,range:kn(e.range)}}))}))}},{key:"provideColorPresentations",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.getColorPresentations(r.toString(),n.color,_n(n.range))})).then((function(e){if(e)return e.map((function(e){var n={label:e.label};return e.textEdit&&(n.textEdit=yn(e.textEdit)),e.additionalTextEdits&&(n.additionalTextEdits=e.additionalTextEdits.map(yn)),n}))}))}}]),e}(),On=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideFoldingRanges",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.getFoldingRanges(r.toString(),n)})).then((function(e){if(e)return e.map((function(e){var n={start:e.startLine+1,end:e.endLine+1};return"undefined"!==typeof e.kind&&(n.kind=function(e){switch(e){case L.Comment:return v.languages.FoldingRangeKind.Comment;case L.Imports:return v.languages.FoldingRangeKind.Imports;case L.Region:return v.languages.FoldingRangeKind.Region}return}(e.kind)),n}))}))}}]),e}();var Nn=function(){function e(n){(0,o.Z)(this,e),this._worker=n}return(0,a.Z)(e,[{key:"provideSelectionRanges",value:function(e,n,t){var r=e.uri;return this._worker(r).then((function(e){return e.getSelectionRanges(r.toString(),n.map(mn))})).then((function(e){if(e)return e.map((function(e){for(var n=[];e;)n.push({range:kn(e.range)}),e=e.parent;return n}))}))}}]),e}();function Un(e){var n=[],t=[],r=new ge(e);n.push(r);var i=function(){return r.getLanguageServiceWorker.apply(r,arguments)};return function(){var n=e.languageId,r=e.modeConfiguration;Vn(t),r.completionItems&&t.push(v.languages.registerCompletionItemProvider(n,new pn(i,["/","-",":"]))),r.hovers&&t.push(v.languages.registerHoverProvider(n,new bn(i))),r.documentHighlights&&t.push(v.languages.registerDocumentHighlightProvider(n,new xn(i))),r.definitions&&t.push(v.languages.registerDefinitionProvider(n,new In(i))),r.references&&t.push(v.languages.registerReferenceProvider(n,new Rn(i))),r.documentSymbols&&t.push(v.languages.registerDocumentSymbolProvider(n,new Dn(i))),r.rename&&t.push(v.languages.registerRenameProvider(n,new Tn(i))),r.colors&&t.push(v.languages.registerColorProvider(n,new jn(i))),r.foldingRanges&&t.push(v.languages.registerFoldingRangeProvider(n,new On(i))),r.diagnostics&&t.push(new hn(n,i,e.onDidChange)),r.selectionRanges&&t.push(v.languages.registerSelectionRangeProvider(n,new Nn(i))),r.documentFormattingEdits&&t.push(v.languages.registerDocumentFormattingEditProvider(n,new Ln(i))),r.documentRangeFormattingEdits&&t.push(v.languages.registerDocumentRangeFormattingEditProvider(n,new Fn(i)))}(),n.push(Wn(t)),Wn(n)}function Wn(e){return{dispose:function(){return Vn(e)}}}function Vn(e){for(;e.length;)e.pop().dispose()}}}]);
//# sourceMappingURL=9214.5198dfc3.chunk.js.map