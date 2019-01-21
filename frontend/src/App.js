import React, { Component } from 'react';

import 'bootstrap';
import 'admin-lte';

import 'bootstrap/dist/css/bootstrap.css';
import 'font-awesome/css/font-awesome.min.css';
import 'ionicons/dist/css/ionicons.min.css';
import 'admin-lte/dist/css/AdminLTE.min.css';
import 'admin-lte/dist/css/skins/skin-blue.css';
import './App.css';

import CCTV from './cctv';

class App extends Component {
  render() {
    return (
      <div className="wrapper skin-blue sidebar-mini">


        <header className="main-header">


          <a href="index2.html" className="logo">
            <span className="logo-mini"><b>A</b>LT</span>
            <span className="logo-lg"><b>Admin</b>LTE</span>
          </a>


          <nav className="navbar navbar-static-top" role="navigation">
            <a href="javascript:;" className="sidebar-toggle" data-toggle="push-menu" role="button">
              <span className="sr-only">Toggle navigation</span>
            </a>
            <div className="navbar-custom-menu">
              <ul className="nav navbar-nav">
                <li className="dropdown messages-menu">
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    <i className="fa fa-envelope-o"></i>
                    <span className="label label-success">4</span>
                  </a>
                  <ul className="dropdown-menu">
                  </ul>
                </li>
                <li className="dropdown notifications-menu">
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    <i className="fa fa-bell-o"></i>
                    <span className="label label-warning">10</span>
                  </a>
                  <ul className="dropdown-menu">
                  </ul>
                </li>
                <li className="dropdown tasks-menu">
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    <i className="fa fa-flag-o"></i>
                    <span className="label label-danger">9</span>
                  </a>
                </li>

                <li className="dropdown user user-menu">
                  <a href="#" className="dropdown-toggle" data-toggle="dropdown">
                    {/* <img src="dist/img/user2-160x160.jpg" className="user-image" alt="User Image" /> */}

                    <span className="hidden-xs">Alexander Pierce</span>
                  </a>
                </li>
                <li>
                  <a href="#" data-toggle="control-sidebar"><i className="fa fa-gears"></i></a>
                </li>
              </ul>
            </div>
          </nav>
        </header>

        <aside className="main-sidebar">
          <section className="sidebar">


            {/* <div className="user-panel">
              <div className="pull-left image">
                <img src="dist/img/user2-160x160.jpg" className="img-circle" alt="User Image" />
              </div>
              <div className="pull-left info">
                <p>Alexander Pierce</p>
                <a href="#"><i className="fa fa-circle text-success"></i> Online</a>
              </div>
            </div> */}


            <form action="#" method="get" className="sidebar-form">
              <div className="input-group">
                <input type="text" name="q" className="form-control" placeholder="Search..." />
                <span className="input-group-btn">
                  <button type="submit" name="search" id="search-btn" className="btn btn-flat"><i className="fa fa-search"></i>
                  </button>
                </span>
              </div>
            </form>



            <ul className="sidebar-menu" data-widget="tree">
              <li className="header">HEADER</li>
              <li className="active"><a href="#"><i className="fa fa-link"></i> <span>Link</span></a></li>
              <li><a href="#"><i className="fa fa-link"></i> <span>Another Link</span></a></li>
              <li className="treeview">
                <a href="#"><i className="fa fa-link"></i> <span>Multilevel</span>
                  <span className="pull-right-container">
                    <i className="fa fa-angle-left pull-right"></i>
                  </span>
                </a>
                <ul className="treeview-menu">
                  <li><a href="#">Link in level 2</a></li>
                  <li><a href="#">Link in level 2</a></li>
                </ul>
              </li>
            </ul>
          </section>
        </aside>


        <div className="content-wrapper">
          <section className="content-header">
            <h1>
              Page Header
            <small>Optional description</small>
            </h1>
            <ol className="breadcrumb">
              <li><a href="#"><i className="fa fa-dashboard"></i> Level</a></li>
              <li className="active">Here</li>
            </ol>
          </section>


          <section className="content container-fluid">
            {/*  | Your Page Content Here | */}
            <CCTV />
          </section>
        </div>



        <footer className="main-footer">
          <div className="pull-right hidden-xs">
            Anything you want
          </div>
          <strong>Copyright &copy; 2016 <a href="#">Company</a>.</strong> All rights reserved.
        </footer>


        <aside className="control-sidebar control-sidebar-dark">
          <ul className="nav nav-tabs nav-justified control-sidebar-tabs">
            <li className="active"><a href="#control-sidebar-home-tab" data-toggle="tab"><i className="fa fa-home"></i></a></li>
            <li><a href="#control-sidebar-settings-tab" data-toggle="tab"><i className="fa fa-gears"></i></a></li>
          </ul>
          <div className="tab-content">
            <div className="tab-pane active" id="control-sidebar-home-tab">  
            </div>
            <div className="tab-pane" id="control-sidebar-stats-tab">Stats Tab Content</div>
            <div className="tab-pane" id="control-sidebar-settings-tab">
            </div>
          </div>
        </aside>
        {/* <!-- Add the sidebar's background. This div must be placed
  immediately after the control sidebar --> */}
        <div className="control-sidebar-bg"></div>
      </div>
    );
  }
}

export default App;
