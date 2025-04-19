import React, { useEffect, useRef } from "react";
import "../css/Modal.css";

const Modal = ({ show, title, messages, onClose }) => {
  const closeBtnRef = useRef();

  useEffect(() => {
    if (show) {
      closeBtnRef.current?.focus();
      const handleKeyDown = (e) => {
        if (e.key === "Escape") onClose();
      };
      document.addEventListener("keydown", handleKeyDown);
      return () => document.removeEventListener("keydown", handleKeyDown);
    }
  }, [show, onClose]);

  if (!show) return null;

  return (
    <div 
      className="modal-backdrop" 
      onClick={onClose}
      role="dialog" 
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 id="modal-title" className="modal-title">{title}</h3>
          <button 
            className="modal-close-icon"
            onClick={onClose}
            aria-label="Close modal"
          >
            &times;
          </button>
        </div>
        
        <ul className="modal-message-list">
          {messages.map((msg, idx) => (
            <li key={idx} className="modal-message">{msg}</li>
          ))}
        </ul>

        <button 
          ref={closeBtnRef}
          className="modal-close-btn" 
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default Modal;