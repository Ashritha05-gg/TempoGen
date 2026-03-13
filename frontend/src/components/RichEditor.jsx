import { useEffect } from "react";
import { EditorContent, useEditor } from "@tiptap/react";
import { BubbleMenu } from "@tiptap/react/menus";

import StarterKit from "@tiptap/starter-kit";
import { TextStyle } from "@tiptap/extension-text-style";
import Color from "@tiptap/extension-color";
import FontFamily from "@tiptap/extension-font-family";
import FontSize from "@tiptap/extension-font-size";
import Highlight from "@tiptap/extension-highlight";
import Underline from "@tiptap/extension-underline";

export default function RichEditor({ content, onChange }) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      TextStyle,
      FontFamily,
      Color,
      FontSize,
      Highlight.configure({ multicolor: true }),
      Underline,
    ],

    content: content || "",

    onUpdate({ editor }) {
      onChange(editor.getHTML());
    },
  });

  // 🔄 Sync AI updates → editor
  useEffect(() => {
    if (!editor) return;

    if (editor.getHTML() !== content) {
      editor.commands.setContent(content || "", false);
    }
  }, [content, editor]);

  if (!editor) return null;

  return (
    <div className="editor-wrapper">

      {/* ⭐ FLOATING SELECTION TOOLBAR */}
      <BubbleMenu editor={editor} tippyOptions={{ duration: 120 }}>
        <div
          style={{
            display: "flex",
            gap: 8,
            background: "#ffffff",
            padding: "8px 10px",
            borderRadius: 10,
            boxShadow: "0 8px 25px rgba(0,0,0,0.18)",
            alignItems: "center",
            fontSize: 14,
          }}
        >
          {/* BOLD */}
          <button onClick={() => editor.chain().focus().toggleBold().run()}>
            <b>B</b>
          </button>

          {/* ITALIC */}
          <button onClick={() => editor.chain().focus().toggleItalic().run()}>
            <i>I</i>
          </button>

          {/* UNDERLINE */}
          <button onClick={() => editor.chain().focus().toggleUnderline().run()}>
            <u>U</u>
          </button>

          {/* Divider */}
          <span style={{ width: 1, height: 18, background: "#ddd" }} />

          {/* FONT FAMILY */}
          <select
            onChange={(e) =>
              editor.chain().focus().setFontFamily(e.target.value).run()
            }
          >
            <option value="">Font</option>
            <option value="Arial">Arial</option>
            <option value="Times New Roman">Times</option>
            <option value="Georgia">Georgia</option>
            <option value="Courier New">Courier</option>
          </select>

          {/* FONT SIZE */}
          <select
            onChange={(e) =>
              editor.chain().focus().setFontSize(e.target.value).run()
            }
          >
            <option value="">Size</option>
            <option value="12px">12</option>
            <option value="14px">14</option>
            <option value="16px">16</option>
            <option value="18px">18</option>
            <option value="24px">24</option>
            <option value="32px">32</option>
            <option value="40px">40</option>
          </select>

          <span style={{ width: 1, height: 18, background: "#ddd" }} />

          {/* TEXT COLOR */}
          <label
            title="Text Color"
            style={{
              display: "flex",
              alignItems: "center",
              gap: 4,
              cursor: "pointer",
            }}
          >
            A
            <input
              type="color"
              style={{
                width: 22,
                height: 22,
                border: "none",
                cursor: "pointer",
              }}
              onChange={(e) =>
                editor.chain().focus().setColor(e.target.value).run()
              }
            />
          </label>

          {/* HIGHLIGHT */}
          <label
            title="Highlight"
            style={{
              display: "flex",
              alignItems: "center",
              gap: 4,
              cursor: "pointer",
            }}
          >
            🖍
            <input
              type="color"
              style={{
                width: 22,
                height: 22,
                border: "none",
                cursor: "pointer",
              }}
              onChange={(e) =>
                editor
                  .chain()
                  .focus()
                  .toggleHighlight({ color: e.target.value })
                  .run()
              }
            />
          </label>
        </div>
      </BubbleMenu>

      {/* 📝 EDITABLE DOCUMENT AREA */}
      <EditorContent editor={editor} className="editor-content" />

    </div>
  );
}
