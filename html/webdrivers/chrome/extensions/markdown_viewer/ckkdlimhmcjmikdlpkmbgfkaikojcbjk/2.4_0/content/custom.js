// let stateCheck = setInterval(() => {
//     if (document.readyState === 'complete'
//         // document.readyState === 'interactive'
//         && typeof jQuery.fn.jquery == 'string') {
//         clearInterval(stateCheck);

//         console.log(jQuery.fn.jquery);
//         console.log(document.body.clientWidth);

//         document.body.attributes['data-screen-width']=document.body.clientWidth;
//         function width_fn() {
//             document.body.attributes['data-screen-width']=document.body.clientWidth;
//         };
//         window.onresize=width_fn;

//         console.log(document.body.attributes['data-screen-width']);
//         //   ].join('; '), runAt: 'document_idle'})

//         // chrome.tabs.executeScript(id, {
//         // code: [
//         // "console.log('ok')"
//         // "document.getElementsByTagName('body')[0].attributes['data-screen-width']=document.getElementsByTagName('body')[0].clientWidth"
//         // ].join('; '), runAt: 'document_idle'})
//     }
// }, 100);
