import{S as Y,i as Z,s as q,w as L,b as c,f as m,g as k,x as M,n as g,B as ne,a5 as P,e as v,Y as B,t as V,a as T,h as D,C as F,l as z,A as ie,d as A,P as ae,c as O,m as R,j as y,k as H,o as S,F as fe,R as ce,T as ue,U as _e,V as de,D as U,E as G}from"./index.cfc0d6fa.js";import{g as me}from"./color.915f3988.js";import{B as ge}from"./BlockLabel.8d7c61d8.js";function he(s){let e,n,l;return{c(){e=L("svg"),n=L("path"),l=L("path"),c(n,"fill","currentColor"),c(n,"d","M12 15H5a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h5V5a1 1 0 0 0-1-1H3V2h6a3 3 0 0 1 3 3zM5 9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h5V9zm15 14v2a1 1 0 0 0 1 1h5v-4h-5a1 1 0 0 0-1 1z"),c(l,"fill","currentColor"),c(l,"d","M2 30h28V2Zm26-2h-7a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h5v-2a1 1 0 0 0-1-1h-6v-2h6a3 3 0 0 1 3 3Z"),c(e,"xmlns","http://www.w3.org/2000/svg"),c(e,"xmlns:xlink","http://www.w3.org/1999/xlink"),c(e,"aria-hidden","true"),c(e,"role","img"),c(e,"class","iconify iconify--carbon"),c(e,"width","100%"),c(e,"height","100%"),c(e,"preserveAspectRatio","xMidYMid meet"),c(e,"viewBox","0 0 32 32")},m(o,r){m(o,e,r),k(e,n),k(e,l)},p:M,i:M,o:M,d(o){o&&g(e)}}}class oe extends Y{constructor(e){super(),Z(this,e,null,he,q,{})}}function J(s,e,n){const l=s.slice();return l[15]=e[n][0],l[22]=e[n][1],l}function K(s,e,n){const l=s.slice();return l[15]=e[n][0],l[16]=e[n][1],l}function Q(s,e,n){const l=s.slice();return l[16]=e[n][0],l[19]=e[n][1],l[21]=n,l}function be(s){let e,n,l=s[1]&&W(),o=s[0],r=[];for(let t=0;t<o.length;t+=1)r[t]=X(J(s,o,t));return{c(){l&&l.c(),e=T(),n=v("div");for(let t=0;t<r.length;t+=1)r[t].c();c(n,"class","textfield p-2 bg-white dark:bg-gray-800 rounded box-border max-w-full break-word leading-7"),c(n,"data-testid","highlighted-text:textfield")},m(t,i){l&&l.m(t,i),m(t,e,i),m(t,n,i);for(let a=0;a<r.length;a+=1)r[a].m(n,null)},p(t,i){if(t[1]?l||(l=W(),l.c(),l.m(e.parentNode,e)):l&&(l.d(1),l=null),i&1){o=t[0];let a;for(a=0;a<o.length;a+=1){const d=J(t,o,a);r[a]?r[a].p(d,i):(r[a]=X(d),r[a].c(),r[a].m(n,null))}for(;a<r.length;a+=1)r[a].d(1);r.length=o.length}},d(t){l&&l.d(t),t&&g(e),t&&g(n),F(r,t)}}}function pe(s){let e,n,l=s[1]&&x(s),o=s[0],r=[];for(let t=0;t<o.length;t+=1)r[t]=le(K(s,o,t));return{c(){l&&l.c(),e=T(),n=v("div");for(let t=0;t<r.length;t+=1)r[t].c();c(n,"class","textfield bg-white dark:bg-transparent rounded-sm text-sm box-border max-w-full break-word leading-7 mt-7"),c(n,"data-testid","highlighted-text:textfield")},m(t,i){l&&l.m(t,i),m(t,e,i),m(t,n,i);for(let a=0;a<r.length;a+=1)r[a].m(n,null)},p(t,i){if(t[1]?l?l.p(t,i):(l=x(t),l.c(),l.m(e.parentNode,e)):l&&(l.d(1),l=null),i&15){o=t[0];let a;for(a=0;a<o.length;a+=1){const d=K(t,o,a);r[a]?r[a].p(d,i):(r[a]=le(d),r[a].c(),r[a].m(n,null))}for(;a<r.length;a+=1)r[a].d(1);r.length=o.length}},d(t){l&&l.d(t),t&&g(e),t&&g(n),F(r,t)}}}function W(s){let e;return{c(){e=v("div"),e.innerHTML=`<span>-1</span> 
			<span>0</span> 
			<span>+1</span>`,c(e,"class","color_legend flex px-2 py-1 justify-between rounded mb-3 font-semibold mt-7"),c(e,"data-testid","highlighted-text:color-legend"),B(e,"background","-webkit-linear-gradient(to right,#8d83d6,(255,255,255,0),#eb4d4b)"),B(e,"background","linear-gradient(to right,#8d83d6,rgba(255,255,255,0),#eb4d4b)")},m(n,l){m(n,e,l)},d(n){n&&g(e)}}}function X(s){let e,n,l=s[15]+"",o,r,t;return{c(){e=v("span"),n=v("span"),o=V(l),r=T(),c(n,"class","text dark:text-white"),c(e,"class","textspan p-1 mr-0.5 bg-opacity-20 dark:bg-opacity-80 rounded-sm"),c(e,"style",t="background-color: rgba("+(s[22]<0?"141, 131, 214,"+-s[22]:"235, 77, 75,"+s[22])+")")},m(i,a){m(i,e,a),k(e,n),k(n,o),k(e,r)},p(i,a){a&1&&l!==(l=i[15]+"")&&D(o,l),a&1&&t!==(t="background-color: rgba("+(i[22]<0?"141, 131, 214,"+-i[22]:"235, 77, 75,"+i[22])+")")&&c(e,"style",t)},d(i){i&&g(e)}}}function x(s){let e,n=Object.entries(s[2]),l=[];for(let o=0;o<n.length;o+=1)l[o]=$(Q(s,n,o));return{c(){e=v("div");for(let o=0;o<l.length;o+=1)l[o].c();c(e,"class","category-legend flex flex-wrap gap-1 mb-2 text-black mt-7"),c(e,"data-testid","highlighted-text:category-legend")},m(o,r){m(o,e,r);for(let t=0;t<l.length;t+=1)l[t].m(e,null)},p(o,r){if(r&100){n=Object.entries(o[2]);let t;for(t=0;t<n.length;t+=1){const i=Q(o,n,t);l[t]?l[t].p(i,r):(l[t]=$(i),l[t].c(),l[t].m(e,null))}for(;t<l.length;t+=1)l[t].d(1);l.length=n.length}},d(o){o&&g(e),F(l,o)}}}function $(s){let e,n=s[16]+"",l,o,r,t,i;function a(){return s[8](s[16])}function d(){return s[9](s[16])}return{c(){e=v("div"),l=V(n),o=T(),c(e,"class","category-label px-2 rounded-sm font-semibold cursor-pointer"),c(e,"style",r="background-color:"+s[19].secondary)},m(u,p){m(u,e,p),k(e,l),k(e,o),t||(i=[z(e,"mouseover",a),z(e,"focus",d),z(e,"mouseout",s[10]),z(e,"blur",s[11])],t=!0)},p(u,p){s=u,p&4&&n!==(n=s[16]+"")&&D(l,n),p&4&&r!==(r="background-color:"+s[19].secondary)&&c(e,"style",r)},d(u){u&&g(e),t=!1,ie(i)}}}function ee(s){let e,n,l=s[16]+"",o,r;return{c(){e=V("\xA0"),n=v("span"),o=V(l),r=T(),c(n,"class","label mr-[-4px] font-bold uppercase text-xs inline-category text-white rounded-sm px-[0.325rem] mt-[0.05rem] py-[0.05rem] transition-colors svelte-o4yfdm"),B(n,"background-color",s[16]===null||s[3]&&s[3]!==s[16]?"":s[2][s[16]].primary,!1)},m(t,i){m(t,e,i),m(t,n,i),k(n,o),m(t,r,i)},p(t,i){i&1&&l!==(l=t[16]+"")&&D(o,l),i&13&&B(n,"background-color",t[16]===null||t[3]&&t[3]!==t[16]?"":t[2][t[16]].primary,!1)},d(t){t&&g(e),t&&g(n),t&&g(r)}}}function le(s){let e,n,l=s[15]+"",o,r,t=!s[1]&&s[16]!==null&&ee(s);return{c(){e=v("span"),n=v("span"),o=V(l),r=T(),t&&t.c(),c(n,"class","text "),c(e,"class","textspan rounded-sm px-1 transition-colors text-black pb-[0.225rem] pt-[0.15rem] svelte-o4yfdm"),A(e,"dark:text-white",s[16]===null||s[3]&&s[3]!==s[16]),A(e,"hl",s[16]!==null),B(e,"background-color",s[16]===null||s[3]&&s[3]!==s[16]?"":s[2][s[16]].secondary,!1)},m(i,a){m(i,e,a),k(e,n),k(n,o),k(e,r),t&&t.m(e,null)},p(i,a){a&1&&l!==(l=i[15]+"")&&D(o,l),!i[1]&&i[16]!==null?t?t.p(i,a):(t=ee(i),t.c(),t.m(e,null)):t&&(t.d(1),t=null),a&9&&A(e,"dark:text-white",i[16]===null||i[3]&&i[3]!==i[16]),a&1&&A(e,"hl",i[16]!==null),a&13&&B(e,"background-color",i[16]===null||i[3]&&i[3]!==i[16]?"":i[2][i[16]].secondary,!1)},d(i){i&&g(e),t&&t.d()}}}function ke(s){let e;function n(r,t){return r[4]==="categories"?pe:be}let l=n(s),o=l(s);return{c(){o.c(),e=ne()},m(r,t){o.m(r,t),m(r,e,t)},p(r,[t]){l===(l=n(r))&&o?o.p(r,t):(o.d(1),o=l(r),o&&(o.c(),o.m(e.parentNode,e)))},i:M,o:M,d(r){o.d(r),r&&g(e)}}}function ve(s,e,n){const l=typeof document<"u";let{value:o=[]}=e,{show_legend:r=!1}=e,{color_map:t={}}=e,i,a={},d="";function u(h,w){if(!i){var j=document.createElement("canvas");i=j.getContext("2d")}i.fillStyle=h,i.fillRect(0,0,1,1);const[I,re,se]=i.getImageData(0,0,1,1).data;return i.clearRect(0,0,1,1),`rgba(${I}, ${re}, ${se}, ${255/w})`}let p;function _(h){n(3,d=h)}function C(){n(3,d="")}const f=h=>_(h),b=h=>_(h),E=()=>C(),N=()=>C();return s.$$set=h=>{"value"in h&&n(0,o=h.value),"show_legend"in h&&n(1,r=h.show_legend),"color_map"in h&&n(7,t=h.color_map)},s.$$.update=()=>{if(s.$$.dirty&129){let h=function(){for(const w in t){const j=t[w].trim();j in P?n(2,a[w]=P[j],a):n(2,a[w]={primary:l?u(t[w],1):t[w],secondary:l?u(t[w],.5):t[w]},a)}};if(t||n(7,t={}),o.length>0){for(let[w,j]of o)if(j!==null)if(typeof j=="string"){if(n(4,p="categories"),!(j in t)){let I=me(Object.keys(t).length);n(7,t[j]=I,t)}}else n(4,p="scores")}h()}},[o,r,a,d,p,_,C,t,f,b,E,N]}class we extends Y{constructor(e){super(),Z(this,e,ve,ke,q,{value:0,show_legend:1,color_map:7})}}function te(s){let e,n;return e=new ge({props:{Icon:oe,label:s[5],disable:typeof s[0].container=="boolean"&&!s[0].container}}),{c(){O(e.$$.fragment)},m(l,o){R(e,l,o),n=!0},p(l,o){const r={};o&32&&(r.label=l[5]),o&1&&(r.disable=typeof l[0].container=="boolean"&&!l[0].container),e.$set(r)},i(l){n||(y(e.$$.fragment,l),n=!0)},o(l){H(e.$$.fragment,l),n=!1},d(l){S(e,l)}}}function ye(s){let e,n,l,o;return l=new oe({}),{c(){e=v("div"),n=v("div"),O(l.$$.fragment),c(n,"class","h-5 dark:text-white opacity-50"),c(e,"class","h-full min-h-[6rem] flex justify-center items-center")},m(r,t){m(r,e,t),k(e,n),R(l,n,null),o=!0},p:M,i(r){o||(y(l.$$.fragment,r),o=!0)},o(r){H(l.$$.fragment,r),o=!1},d(r){r&&g(e),S(l)}}}function je(s){let e,n;return e=new we({props:{value:s[3],show_legend:s[4],color_map:s[0].color_map}}),{c(){O(e.$$.fragment)},m(l,o){R(e,l,o),n=!0},p(l,o){const r={};o&8&&(r.value=l[3]),o&16&&(r.show_legend=l[4]),o&1&&(r.color_map=l[0].color_map),e.$set(r)},i(l){n||(y(e.$$.fragment,l),n=!0)},o(l){H(e.$$.fragment,l),n=!1},d(l){S(e,l)}}}function He(s){let e,n,l,o,r,t,i;const a=[s[6]];let d={};for(let f=0;f<a.length;f+=1)d=ce(d,a[f]);e=new ue({props:d});let u=s[5]&&te(s);const p=[je,ye],_=[];function C(f,b){return f[3]?0:1}return o=C(s),r=_[o]=p[o](s),{c(){O(e.$$.fragment),n=T(),u&&u.c(),l=T(),r.c(),t=ne()},m(f,b){R(e,f,b),m(f,n,b),u&&u.m(f,b),m(f,l,b),_[o].m(f,b),m(f,t,b),i=!0},p(f,b){const E=b&64?_e(a,[de(f[6])]):{};e.$set(E),f[5]?u?(u.p(f,b),b&32&&y(u,1)):(u=te(f),u.c(),y(u,1),u.m(l.parentNode,l)):u&&(U(),H(u,1,1,()=>{u=null}),G());let N=o;o=C(f),o===N?_[o].p(f,b):(U(),H(_[N],1,1,()=>{_[N]=null}),G(),r=_[o],r?r.p(f,b):(r=_[o]=p[o](f),r.c()),y(r,1),r.m(t.parentNode,t))},i(f){i||(y(e.$$.fragment,f),y(u),y(r),i=!0)},o(f){H(e.$$.fragment,f),H(u),H(r),i=!1},d(f){S(e,f),f&&g(n),u&&u.d(f),f&&g(l),_[o].d(f),f&&g(t)}}}function Te(s){let e,n;return e=new ae({props:{test_id:"highlighted-text",visible:s[2],elem_id:s[1],disable:typeof s[0].container=="boolean"&&!s[0].container,$$slots:{default:[He]},$$scope:{ctx:s}}}),{c(){O(e.$$.fragment)},m(l,o){R(e,l,o),n=!0},p(l,[o]){const r={};o&4&&(r.visible=l[2]),o&2&&(r.elem_id=l[1]),o&1&&(r.disable=typeof l[0].container=="boolean"&&!l[0].container),o&633&&(r.$$scope={dirty:o,ctx:l}),e.$set(r)},i(l){n||(y(e.$$.fragment,l),n=!0)},o(l){H(e.$$.fragment,l),n=!1},d(l){S(e,l)}}}function Ce(s,e,n){let{elem_id:l=""}=e,{visible:o=!0}=e,{value:r}=e,{show_legend:t}=e,{color_map:i={}}=e,{label:a}=e,{style:d={}}=e,{loading_status:u}=e;const p=fe();return s.$$set=_=>{"elem_id"in _&&n(1,l=_.elem_id),"visible"in _&&n(2,o=_.visible),"value"in _&&n(3,r=_.value),"show_legend"in _&&n(4,t=_.show_legend),"color_map"in _&&n(7,i=_.color_map),"label"in _&&n(5,a=_.label),"style"in _&&n(0,d=_.style),"loading_status"in _&&n(6,u=_.loading_status)},s.$$.update=()=>{s.$$.dirty&129&&!d.color_map&&Object.keys(i).length&&n(0,d.color_map=i,d),s.$$.dirty&8&&p("change")},[d,l,o,r,t,a,u,i]}class Me extends Y{constructor(e){super(),Z(this,e,Ce,Te,q,{elem_id:1,visible:2,value:3,show_legend:4,color_map:7,label:5,style:0,loading_status:6})}}var Oe=Me;const Re=["static"],Se=s=>({type:"Array<[string, string | number]>",description:"list of text spans and corresponding label / value"});export{Oe as Component,Se as document,Re as modes};
//# sourceMappingURL=index.075e5aff.js.map
