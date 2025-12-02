// import axios from "axios";

// export default function UploadPanel({ onUploadSuccess, setDocumentContent }) {

//   const handleUpload = async (e) => {
//     const files = e.target.files;
//     if (!files.length) return;

//     const formData = new FormData();
//     for (let f of files) {
//       formData.append("files", f);
//     }

//     try {
//       const res = await axios.post(
//         "http://127.0.0.1:8000/upload_files",
//         formData
//       );

//       // ✅ SET EXTRACTED CONTENT TO PREVIEW
//       if (res.data?.content) {
//         setDocumentContent(res.data.content);
//       }

//       onUploadSuccess(); // ✅ switch to document preview

//     } catch (err) {
//       console.error(err);
//       alert("File upload failed");
//     }
//   };

//   return (
//     <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
//       <h3>Upload Source Materials</h3>

//       <label className="upload-box">
//         <input
//           type="file"
//           multiple
//           hidden
//           onChange={handleUpload}
//           accept=".pdf,.docx,.ppt,.pptx,.xls,.xlsx"
//         />
//         ☁️
//         <p>Drop PDF, PPT, Excel, DOCX files here</p>
//         <span>or click to browse</span>
//       </label>

//       <div style={{ marginTop: "auto" }}>
//         <button className="primary-btn" type="button">
//           Submit & Preview
//         </button>
//       </div>
//     </div>
//   );
// }

import axios from "axios";

export default function UploadPanel({ onUploadSuccess }) {

  const handleUpload = async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const formData = new FormData();
    for (let file of files) {
      formData.append("files", file);
    }

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/upload_files",
        formData
      );

      console.log("UPLOAD SUCCESS:", res.data);
      onUploadSuccess();

    } catch (err) {
      console.error("UPLOAD ERROR:", err?.response || err.message);
      alert("Upload failed. Check console.");
    }
  };

  return (
    <>
      <h3>Upload Source Materials</h3>

      <label className="upload-box">
        <input
          type="file"
          multiple
          hidden
          onChange={handleUpload}
          accept=".pdf,.docx,.ppt,.pptx,.xls,.xlsx"
        />
        ☁️
        <p>Drop PDF, PPT, Excel, DOCX files here</p>
        <span>or click to browse</span>
      </label>
    </>
  );
}
