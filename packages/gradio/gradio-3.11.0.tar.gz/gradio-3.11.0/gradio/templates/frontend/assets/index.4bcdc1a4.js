import{S as V,i as Z,s as A,w as E,b as d,f as g,g as b,x as H,n as h,B as z,e as v,a as j,t as N,Y as R,h as D,C as K,d as C,P as O,c as L,m as M,j as p,k as w,o as B,F as Q,R as W,T as X,U as x,V as $,D as T,E as Y}from"./index.2e8e82ba.js";import{B as ee}from"./BlockLabel.17413437.js";function le(a){let e,n;return{c(){e=E("svg"),n=E("path"),d(n,"fill","currentColor"),d(n,"d","M4 2H2v26a2 2 0 0 0 2 2h26v-2H4v-3h22v-8H4v-4h14V5H4Zm20 17v4H4v-4ZM16 7v4H4V7Z"),d(e,"xmlns","http://www.w3.org/2000/svg"),d(e,"xmlns:xlink","http://www.w3.org/1999/xlink"),d(e,"aria-hidden","true"),d(e,"role","img"),d(e,"class","iconify iconify--carbon"),d(e,"width","100%"),d(e,"height","100%"),d(e,"preserveAspectRatio","xMidYMid meet"),d(e,"viewBox","0 0 32 32")},m(l,t){g(l,e,t),b(e,n)},p:H,i:H,o:H,d(l){l&&h(e)}}}class G extends V{constructor(e){super(),Z(this,e,null,le,A,{})}}function q(a,e,n){const l=a.slice();return l[2]=e[n],l}function F(a){let e,n=a[0].confidences,l=[];for(let t=0;t<n.length;t+=1)l[t]=P(q(a,n,t));return{c(){for(let t=0;t<l.length;t+=1)l[t].c();e=z()},m(t,i){for(let s=0;s<l.length;s+=1)l[s].m(t,i);g(t,e,i)},p(t,i){if(i&1){n=t[0].confidences;let s;for(s=0;s<n.length;s+=1){const o=q(t,n,s);l[s]?l[s].p(o,i):(l[s]=P(o),l[s].c(),l[s].m(e.parentNode,e))}for(;s<l.length;s+=1)l[s].d(1);l.length=n.length}},d(t){K(l,t),t&&h(e)}}}function I(a){let e,n,l,t=Math.round(a[2].confidence*100)+"",i,s;return{c(){e=v("div"),n=j(),l=v("div"),i=N(t),s=N("%"),d(e,"class","flex-1 border border-dashed border-gray-100 px-4"),d(l,"class","text-right ml-auto")},m(o,c){g(o,e,c),g(o,n,c),g(o,l,c),b(l,i),b(l,s)},p(o,c){c&1&&t!==(t=Math.round(o[2].confidence*100)+"")&&D(i,t)},d(o){o&&h(e),o&&h(n),o&&h(l)}}}function P(a){let e,n,l,t,i,s,o=a[2].label+"",c,k,u,r=a[0].confidences&&I(a);return{c(){e=v("div"),n=v("div"),l=v("div"),t=j(),i=v("div"),s=v("div"),c=N(o),k=j(),r&&r.c(),u=j(),d(l,"class","h-1 mb-1 rounded bg-gradient-to-r group-hover:from-orange-500 from-orange-400 to-orange-200 dark:from-orange-400 dark:to-orange-600"),R(l,"width",a[2].confidence*100+"%"),d(s,"class","leading-snug"),d(i,"class","flex items-baseline space-x-2 group-hover:text-orange-500"),d(n,"class","flex-1"),d(e,"class","flex items-start justify-between font-mono text-sm leading-none group mb-2 last:mb-0 dark:text-slate-300")},m(_,y){g(_,e,y),b(e,n),b(n,l),b(n,t),b(n,i),b(i,s),b(s,c),b(i,k),r&&r.m(i,null),b(e,u)},p(_,y){y&1&&R(l,"width",_[2].confidence*100+"%"),y&1&&o!==(o=_[2].label+"")&&D(c,o),_[0].confidences?r?r.p(_,y):(r=I(_),r.c(),r.m(i,null)):r&&(r.d(1),r=null)},d(_){_&&h(e),r&&r.d()}}}function te(a){let e,n,l=a[0].label+"",t,i,s=typeof a[0]=="object"&&a[0].confidences&&F(a);return{c(){e=v("div"),n=v("div"),t=N(l),i=j(),s&&s.c(),d(n,"class","output-class font-bold text-2xl py-6 px-4 flex-grow flex items-center justify-center dark:text-slate-200"),C(n,"sr-only",!a[1]),C(n,"no-confidence",!("confidences"in a[0])),d(e,"class","output-label")},m(o,c){g(o,e,c),b(e,n),b(n,t),b(e,i),s&&s.m(e,null)},p(o,[c]){c&1&&l!==(l=o[0].label+"")&&D(t,l),c&2&&C(n,"sr-only",!o[1]),c&1&&C(n,"no-confidence",!("confidences"in o[0])),typeof o[0]=="object"&&o[0].confidences?s?s.p(o,c):(s=F(o),s.c(),s.m(e,null)):s&&(s.d(1),s=null)},i:H,o:H,d(o){o&&h(e),s&&s.d()}}}function ne(a,e,n){let{value:l}=e,{show_label:t}=e;return a.$$set=i=>{"value"in i&&n(0,l=i.value),"show_label"in i&&n(1,t=i.show_label)},[l,t]}class ie extends V{constructor(e){super(),Z(this,e,ne,te,A,{value:0,show_label:1})}}function U(a){let e,n;return e=new ee({props:{Icon:G,label:a[3],disable:typeof a[4].container=="boolean"&&!a[4].container}}),{c(){L(e.$$.fragment)},m(l,t){M(e,l,t),n=!0},p(l,t){const i={};t&8&&(i.label=l[3]),t&16&&(i.disable=typeof l[4].container=="boolean"&&!l[4].container),e.$set(i)},i(l){n||(p(e.$$.fragment,l),n=!0)},o(l){w(e.$$.fragment,l),n=!1},d(l){B(e,l)}}}function se(a){let e,n,l,t;return l=new G({}),{c(){e=v("div"),n=v("div"),L(l.$$.fragment),d(n,"class","h-5 dark:text-white opacity-50"),d(e,"class","h-full min-h-[6rem] flex justify-center items-center")},m(i,s){g(i,e,s),b(e,n),M(l,n,null),t=!0},p:H,i(i){t||(p(l.$$.fragment,i),t=!0)},o(i){w(l.$$.fragment,i),t=!1},d(i){i&&h(e),B(l)}}}function ae(a){let e,n;return e=new ie({props:{value:a[2],show_label:a[6]}}),{c(){L(e.$$.fragment)},m(l,t){M(e,l,t),n=!0},p(l,t){const i={};t&4&&(i.value=l[2]),t&64&&(i.show_label=l[6]),e.$set(i)},i(l){n||(p(e.$$.fragment,l),n=!0)},o(l){w(e.$$.fragment,l),n=!1},d(l){B(e,l)}}}function oe(a){let e,n,l,t,i,s,o;const c=[a[5]];let k={};for(let f=0;f<c.length;f+=1)k=W(k,c[f]);e=new X({props:k});let u=a[6]&&U(a);const r=[ae,se],_=[];function y(f,m){return typeof f[2]=="object"&&f[2]!==void 0&&f[2]!==null?0:1}return t=y(a),i=_[t]=r[t](a),{c(){L(e.$$.fragment),n=j(),u&&u.c(),l=j(),i.c(),s=z()},m(f,m){M(e,f,m),g(f,n,m),u&&u.m(f,m),g(f,l,m),_[t].m(f,m),g(f,s,m),o=!0},p(f,m){const J=m&32?x(c,[$(f[5])]):{};e.$set(J),f[6]?u?(u.p(f,m),m&64&&p(u,1)):(u=U(f),u.c(),p(u,1),u.m(l.parentNode,l)):u&&(T(),w(u,1,1,()=>{u=null}),Y());let S=t;t=y(f),t===S?_[t].p(f,m):(T(),w(_[S],1,1,()=>{_[S]=null}),Y(),i=_[t],i?i.p(f,m):(i=_[t]=r[t](f),i.c()),p(i,1),i.m(s.parentNode,s))},i(f){o||(p(e.$$.fragment,f),p(u),p(i),o=!0)},o(f){w(e.$$.fragment,f),w(u),w(i),o=!1},d(f){B(e,f),f&&h(n),u&&u.d(f),f&&h(l),_[t].d(f),f&&h(s)}}}function fe(a){let e,n;return e=new O({props:{test_id:"label",visible:a[1],elem_id:a[0],disable:typeof a[4].container=="boolean"&&!a[4].container,$$slots:{default:[oe]},$$scope:{ctx:a}}}),{c(){L(e.$$.fragment)},m(l,t){M(e,l,t),n=!0},p(l,[t]){const i={};t&2&&(i.visible=l[1]),t&1&&(i.elem_id=l[0]),t&16&&(i.disable=typeof l[4].container=="boolean"&&!l[4].container),t&380&&(i.$$scope={dirty:t,ctx:l}),e.$set(i)},i(l){n||(p(e.$$.fragment,l),n=!0)},o(l){w(e.$$.fragment,l),n=!1},d(l){B(e,l)}}}function re(a,e,n){let{elem_id:l=""}=e,{visible:t=!0}=e,{value:i}=e,{label:s="Label"}=e,{style:o={}}=e,{loading_status:c}=e,{show_label:k}=e;const u=Q();return a.$$set=r=>{"elem_id"in r&&n(0,l=r.elem_id),"visible"in r&&n(1,t=r.visible),"value"in r&&n(2,i=r.value),"label"in r&&n(3,s=r.label),"style"in r&&n(4,o=r.style),"loading_status"in r&&n(5,c=r.loading_status),"show_label"in r&&n(6,k=r.show_label)},a.$$.update=()=>{a.$$.dirty&4&&u("change")},[l,t,i,s,o,c,k]}class ce extends V{constructor(e){super(),Z(this,e,re,fe,A,{elem_id:0,visible:1,value:2,label:3,style:4,loading_status:5,show_label:6})}}var _e=ce;const be=["static"],me=a=>({type:"{ label: string; confidences?: Array<{ label: string; confidence: number }>",description:"output label and optional set of confidences per label"});export{_e as Component,me as document,be as modes};
//# sourceMappingURL=index.4bcdc1a4.js.map
