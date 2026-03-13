import "./AboutUs.css";

export default function AboutUs() {
  return (
    <div className="about-page">

      <div className="about-container">

        <h1 className="about-title">About TempOGen</h1>

        <p className="about-intro">
          TempOGen is an AI-powered document generation platform designed
          to simplify the creation of professional documents such as
          academic reports, business reports, and resumes.
        </p>

        <div className="about-section">
          <h2>Our Goal</h2>
          <p>
            The goal of TempOGen is to reduce the time and effort required
            to create well-structured documents. Users can upload reference
            documents and interact with the AI assistant using natural
            language to generate content automatically.
          </p>
        </div>

        <div className="about-section">
          <h2>Key Features</h2>

          <ul>
            <li>AI powered document generation</li>
            <li>Retrieval-Augmented Generation (RAG)</li>
            <li>Live editable document preview</li>
            <li>Professional PDF export</li>
            <li>Resume generation with templates</li>
            <li>Supports multiple file formats</li>
          </ul>
        </div>

        <div className="about-section">
          <h2>Technologies Used</h2>

          <ul>
            <li>React.js for frontend</li>
            <li>FastAPI backend</li>
            <li>Google Gemini AI</li>
            <li>Vector database for document retrieval</li>
            <li>ReportLab for PDF generation</li>
          </ul>
        </div>

        <div className="about-section">
          <h2>Project Overview</h2>

          <p>
            This system integrates Artificial Intelligence with Retrieval
            Augmented Generation techniques to generate structured and
            meaningful content based on uploaded documents and user
            prompts. The platform also provides live editing tools and
            customizable templates to export documents in professional
            formats.
          </p>
        </div>

      </div>

    </div>
  );
}