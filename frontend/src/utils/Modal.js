import React, { Component } from 'react';
import $ from 'jquery';

$(document.body).on('shown.bs.modal,hidden.bs.modal', function () {
  $('body').css('padding-right', '0');
});

class Modal extends Component {

  show() {
    $(this.modal).modal('show');
  }
  hide() {
    $(this.modal).modal('hide');
  } 
  
  render() {
    const { body, title, footer, sm, lg } = this.props;
    let clazz = "modal-dialog";
    if(sm){
      clazz += " modal-sm";
    }else if (lg) {
      clazz += " modal-lg";
    }
    return <div ref={el => {this.modal=el;}} className="modal fade" role="dialog">
      <div className={clazz} role="document">
        <div className="modal-content">

          <div className="modal-header">
            <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 className="modal-title">{title}</h4>
          </div>

          <div className="modal-body">
            {body}
          </div>

          {footer || <div className="modal-footer text-center">
            <button type="button" className="btn btn-primary"
              onClick={e => {
                const { onConfirm } = this.props;
                onConfirm && onConfirm();
                this.hide();
              }}>确定</button>
            <button type="button" className="btn btn-default" data-dismiss="modal"
              onClick={e => {
                const { onCancel } = this.props;
                onCancel && onCancel();
              }}>关闭</button>
          </div>}
        </div>
      </div>
    </div>
  }
};

Modal.defaultProps = {
  title: 'default title', body: 'default body', footer: null,
  onConfirm: null, onCancel: null,
  sm: false, lg: false
};

export default Modal;