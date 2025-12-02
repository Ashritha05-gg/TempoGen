// import Navbar from "./components/Navbar";
// import UploadPanel from "./components/UploadPanel";
// import ChatPanel from "./components/ChatPanel";
// import "./App.css";

// function App() {
//   return (
//     <div className="app-bg">
//       <Navbar />

//       <div className="main-container">
//         <UploadPanel />
//         <ChatPanel />
//       </div>

//       {/* <footer className="footer">
//         © 2025 AI-Powered Template Generation Engine. All rights reserved.
//       </footer> */}
//     </div>
//   );
// }

// export default App;


import { useState } from "react";
import Navbar from "./components/Navbar";
import UploadPanel from "./components/UploadPanel";
import ChatPanel from "./components/ChatPanel";
import Preview from "./components/preview";
import "./App.css";

// function App() {
//   const [documentContent, setDocumentContent] = useState("");
//   const [hasUploaded, setHasUploaded] = useState(false);

//   return (
//     <div className="app-bg">
//       <Navbar />

//       <div className="main-container">
        
//         {/* LEFT PANEL */}
//         <div className="card">
//           {!hasUploaded ? (
//             <UploadPanel
//   onUploadSuccess={() => setHasUploaded(true)}
//   setDocumentContent={setDocumentContent}
// />

//             //<UploadPanel onUploadSuccess={() => setHasUploaded(true)} />
//           ) : (
//             <Preview content={documentContent} />
//           )}
//         </div>

//         {/* RIGHT PANEL */}
//         <div className="card">
//           <ChatPanel setDocumentContent={setDocumentContent} />
//         </div>

//       </div>
//     </div>
//   );
// }

// function App() {
//   const [docSections, setDocSections] = useState([]);
//   const [uploaded, setUploaded] = useState(false);

//   return (
//     <div className="app-bg">
//       <Navbar/>
//       <div className="main-container">
        
//         {/* LEFT PANEL */}
//         <div className="card">
//           {!uploaded ? (
//             <UploadPanel onUploadSuccess={() => setUploaded(true)} />
//           ) : (
//             <Preview sections={docSections} />
//           )}
//         </div>

//         {/* RIGHT PANEL */}
//         <ChatPanel onUpdateDocument={setDocSections} />
//       </div>
//     </div>
//   );
// }
// export default App;


function App() {
  const [docSections, setDocSections] = useState([]);
  const [uploaded, setUploaded] = useState(false);

  return (
    <div className="app-bg">
      <Navbar />

      <div className="main-container">
        {/* LEFT PANEL */}
        <div className="card">
          {!uploaded ? (
            <UploadPanel onUploadSuccess={() => setUploaded(true)} />
          ) : (
            <Preview sections={docSections} />
          )}
        </div>

        {/* RIGHT PANEL */}
        <ChatPanel
          sections={docSections}
          onUpdateDocument={setDocSections}
        />
      </div>
    </div>
  );
}

export default App;
