import axios from "axios";

export default function FileUpload() {

  const uploadFiles = async (e) => {
    const files = e.target.files;
    if (!files.length) return;

    const formData = new FormData();
    for (let f of files) {
      formData.append("files", f);
    }

    await axios.post("http://127.0.0.1:8000/upload_files", formData);
    alert("Files uploaded successfully");
  };

  return (
    <div style={{ padding: "20px", borderBottom: "1px solid #ccc" }}>
      <input type="file" multiple onChange={uploadFiles} />
    </div>
  );
}
