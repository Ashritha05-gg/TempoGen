/* Resume_Templates.jsx*/
import React from "react";
import Navbar from "./Navbar";
import "./Resume_Template.css";

const ResumeTemplateSelect = () => {
  return (
    <>
      

      <div className="resume-template-container">
        <h1 className="page-title">
          Please select template for resume from below
        </h1>
        <p className="page-subtitle">
          Choose a layout style for your resume
        </p>

        <div className="template-grid">
          <div className="template-card">
            <h3>Minimal Resume</h3>
            <p className="template-heading">Sample heading</p>
            <p className="template-preview">
              Sample paragraph preview text...
            </p>
            <p className="template-spacing">Spacing 1.8</p>
          </div>

          <div className="template-card">
            <h3>Hybrid Resume</h3>
            <p className="template-heading">Sample heading</p>
            <p className="template-preview">
              Sample paragraph preview text...
            </p>
            <p className="template-spacing">Spacing 1.4</p>
          </div>

          <div className="template-card">
            <h3>Functional Resume</h3>
            <p className="template-heading">Sample heading</p>
            <p className="template-preview">
              Sample paragraph preview text...
            </p>
            <p className="template-spacing">Spacing 1.4</p>
          </div>

          <div className="template-card">
            <h3>Academic Resume</h3>
            <p className="template-heading">Sample heading</p>
            <p className="template-preview">
              Sample paragraph preview text...
            </p>
            <p className="template-spacing">Spacing 1.6</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default ResumeTemplateSelect;