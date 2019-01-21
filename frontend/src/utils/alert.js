// const React = require('react');
// const ReactDOM = require('react-dom');

// const debounce = require('lodash/debounce');

// const Alert = React.createClass({
//   getInitialState() {
//     return { elems: []};
//   },
//   componentWillMount() {
//     const { elems } = this.state;
//     const _this = this;
//     this.debounce1 = debounce(() => {
//       _this.remove(0); 
//     }, 1000);
//     this.debounce5 = debounce(() => {
//       _this.remove(0); 
//     }, 5000);
//   },
//   add(msg, clazz, args){
//     const { elems} = this.state;
//     const newelems = [...elems, {msg, clazz, args}];
//     newelems.length > 3 && newelems.shift();
//     this.setState({ elems: newelems});
//     this.debounce5();
//   },
//   remove (index) {
//     const { elems } = this.state;
//     elems.length && elems.splice(index, 1);
//     elems.length && this.debounce1();
//     const newelems = [...elems];
//     this.setState({ elems: newelems });
//   },
//   render() {
//     const { elems } = this.state;
//     return <div className="alert-fixed"> 
//       { elems.map((elem, index) => <div 
//         className={"alert alert-dismissible "+elem.clazz} key={index}>

//         {elem.args && elem.args.danger && <span className="glyphicon glyphicon-exclamation-sign" 
//           aria-hidden="true"></span>}
//         {elem.args && elem.args.success && <span className="glyphicon glyphicon-ok"
//           aria-hidden="true"></span>}
//         {elem.args && elem.args.warn && <span className="glyphicon glyphicon-warning-sign"
//           aria-hidden="true"></span>}
//         {elem.args && elem.args.info && <span className="glyphicon glyphicon-bullhorn"
//           aria-hidden="true"></span>}

//         <span className="msgbox"> { elem.msg } </span>
//         <button type="button" className="close" onClick={this.remove.bind(this, index)}>
//           <span aria-hidden="true">&times;</span>
//         </button>

//       </div > )}
//   </div >;
//   }
// });

// var div = document.createElement("div"); 
// var __alert__ = ReactDOM.render(<Alert />, div);
// document.body.appendChild(div)

export const Success = function (message){ 
  // __alert__.add(message, 'alert-success', { success: true });
}

export const Warn = function (message) {
  // __alert__.add(message, 'alert-warning', { warn: true });
}

export const Danger = function (message) {
  // __alert__.add(message, 'alert-danger', { danger: true });
}

export const Info = function (message) {
  // __alert__.add(message, 'alert-info', { info: true });
}