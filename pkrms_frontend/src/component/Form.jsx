import React, { useState, useEffect, useCallback } from "react";
import * as XLSX from "xlsx";
import "../css/Form.css";
import { fetchProvinceList, filterKabupatenList } from "../Services/services";
import { motion } from "framer-motion";

function Form() {
  const [status, setStatus] = useState("");
  const [selectedProvince, setSelectedProvince] = useState("");
  const [selectedKabupaten, setSelectedKabupaten] = useState("");
  const [provinces, setProvinces] = useState([]);
  const [kabupatenList, setKabupatenList] = useState([]);
  const [errors, setErrors] = useState(null);
  const [isErrorPopupOpen, setIsErrorPopupOpen] = useState(false);
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [showAllErrors, setShowAllErrors] = useState(false);

  const [FormData, setFormData] = useState({
    provincial: { lgName: "", email: "", phone: "" },
    kabupaten: { lgName: "", email: "", phone: "" },
  });

  const [files, setFiles] = useState({
    BridgeInventory: null,
    CODE_AN_Parameters: null,
    CODE_AN_UnitCostsPER: null,
    CODE_AN_UnitCostsPERUnpaved: null,
    CODE_AN_UnitCostsREH: null,
    CODE_AN_UnitCostsRIGID: null,
    CODE_AN_UnitCostsRM: null,
    CODE_AN_UnitCostsUPGUnpaved: null,
    CODE_AN_UnitCostsWidening: null,
    CODE_AN_WidthStandards: null,
    CulvertCondition: null,
    CulvertInventory: null,
    Link: null,
    RetainingWallInventory: null,
    RoadInventory: null,
    TrafficVolume: null,
    RoadCondition: null,
  });

  const [excelJson, setExcelJson] = useState({});
  const [output, setOutput] = useState(null);

  useEffect(() => {
    setProvinces(fetchProvinceList());
  }, []);

  const handleProvinceChange = useCallback(
    (e) => {
      const selectedLG = e.target.value;
      const province = provinces.find((p) => p.LG === selectedLG);
      if (!province) return;

      setSelectedProvince(selectedLG);
      setSelectedKabupaten("");
      setKabupatenList(filterKabupatenList(province.adm_code));
    },
    [provinces]
  );

  const handleInputChange = useCallback((e, type, field) => {
    const value = e.target.value;
    setFormData((prev) => ({
      ...prev,
      [type]: { ...prev[type], [field]: value },
    }));
  }, []);

  const handleFileChange = useCallback(async (e, key) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const data = await file.arrayBuffer();
      const workbook = XLSX.read(data, { type: "buffer" });
      
      // Process all sheets in the workbook
      const allData = {};
      workbook.SheetNames.forEach(sheetName => {
        const jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
        allData[sheetName] = jsonData;
      });

      setFiles((prev) => ({ ...prev, [key]: file }));
      setExcelJson((prev) => ({ ...prev, [key]: allData[workbook.SheetNames[0]] }));
    } catch (error) {
      console.error('Error reading Excel file:', error);
      setErrors({ 
        fileError: { 
          title: 'File Error', 
          errors: { [key]: `Error reading Excel file: ${error.message}` } 
        } 
      });
      setIsErrorPopupOpen(true);
    }
  }, []);

  const removeFile = useCallback((key) => {
    setFiles((prev) => ({ ...prev, [key]: null }));
    setExcelJson((prev) => {
      const updated = { ...prev };
      delete updated[key];
      return updated;
    });
  }, []);

  const validateInputs = () => {
    const errors = {};

    if (!status) {
      errors.status = 'Please select a status';
    }

    if (!selectedProvince) {
      errors.province = 'Please select a province';
    }

    if (status === "kabupaten" && !selectedKabupaten) {
      errors.kabupaten = 'Please select a kabupaten';
    }

    const { lgName, email, phone } = FormData[status] || {};

    if (!lgName?.trim()) {
      errors.lgName = 'LG Name is required';
    }

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
      errors.email = 'Please enter a valid email address';
    }

    const phoneRegex = /^[0-9]{9,14}$/;
    if (!phoneRegex.test(phone?.replace(/^\+62/, ''))) {
      errors.phone = 'Phone number must be 9 to 14 digits';
    }

    if (Object.keys(errors).length > 0) {
      setErrors({
        formValidation: {
          title: 'Form Validation Errors',
          errors: errors
        }
      });
      setIsErrorPopupOpen(true);
      return false;
    }

    return true;
  };

  const handleSubmit = async () => {
    if (!validateInputs()) return;

    const prependPrefix = (phone) => {
      if (!phone) return "";
      return phone.startsWith("+62") ? phone : `+62${phone.replace(/^0+/, "")}`;
    };

    const currentFormData = FormData[status];
    const preparedFormData = {
      status: status,
      selected_province: selectedProvince,
      selected_kabupaten: status === "kabupaten" ? selectedKabupaten : null,
      lg_name: currentFormData.lgName,
      email: currentFormData.email,
      phone: prependPrefix(currentFormData.phone)
    };
    
    const jsonData = {
      FormData: [preparedFormData]
    };

    Object.entries(excelJson).forEach(([key, data]) => {
      if (data && Array.isArray(data)) {
        jsonData[key] = data;
      }
    });

    console.group('Form Submission');
    console.log('Submitting data:', jsonData);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload-data/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
      });

      const responseData = await response.json();
      console.log('Server response:', responseData);

      if (!response.ok) {
        if (responseData.status === 'validation_error') {
          const fileErrors = responseData.details?.file_errors || {};
          const formErrors = responseData.details?.FormData || {};
        
          let formattedErrors = {};
        
          // FormData Errors
          if (formErrors.errors) {
            formattedErrors.FormData = {
              type: 'validation_error',
              title: "Form Errors",
              errors: {}
            };
            for (const [field, error] of Object.entries(formErrors.errors)) {
              formattedErrors.FormData.errors[field] = error.errors.join(", ");
            }
          }
        
          // File Errors
          if (Object.keys(fileErrors).length > 0) {
            for (const [fileName, records] of Object.entries(fileErrors)) {
              formattedErrors[fileName] = {
                type: 'validation_error',
                title: `${fileName} Errors`,
                errors: {}
              };
              records.forEach((err) => {
                const message = `${err.field} - ${err.message}`;
                formattedErrors[fileName].errors[`Record ${err.record}`] = message;
              });
            }
          }
          
          setErrors(formattedErrors);
          setSubmissionStatus('error');
          setIsErrorPopupOpen(true);
          return;
        }
        
        throw new Error(responseData.message || `HTTP error! status: ${response.status}`);
      }

      // Handle success response
      if (responseData.status === 'success') {
        console.group('Success Response');
        console.log('Full Response:', responseData);
        console.log('Status:', responseData.status);
        console.log('Message:', responseData.message);
        console.groupEnd();

        setSubmissionStatus('success');
        setErrors({
          success: {
            type: 'success',
            title: 'Success',
            errors: {
              message: responseData.message
            }
          }
        });
        setIsErrorPopupOpen(true);
      } else if (responseData.status === 'partial_success') {
        console.log('Partial Success:', responseData);
        const formattedErrors = {};
        
        // Format successful models
        if (responseData.successful_models && responseData.successful_models.length > 0) {
          formattedErrors.successful_models = {
            type: 'success',
            title: 'Successfully Processed Models',
            errors: {}
          };
          responseData.successful_models.forEach(model => {
            formattedErrors.successful_models.errors[model] = 'Successfully processed';
            console.log(`Successfully processed model: ${model}`);
          });
        } else {
          console.log('No successful models found');
        }
        
        // Format error details
        if (responseData.errors) {
          Object.entries(responseData.errors).forEach(([model, records]) => {
            formattedErrors[model] = {
              type: 'validation_error',
              title: `${model} Errors`,
              errors: {}
            };
            
            Object.entries(records).forEach(([recordKey, errorData]) => {
              const recordNumber = recordKey.split('_').pop();
              const errorMessage = Array.isArray(errorData.errors) 
                ? errorData.errors.join(', ') 
                : Object.entries(errorData.errors)
                    .map(([field, errors]) => `${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`)
                    .join('; ');
              
              formattedErrors[model].errors[`Record ${recordNumber}`] = errorMessage;
              console.log(`Error in ${model} - Record ${recordNumber}:`, errorMessage);
            });
          });
        } else {
          console.log('No errors found');
        }
        
        setSubmissionStatus('partial_success');
        setErrors(formattedErrors);
        setIsErrorPopupOpen(true);
      } else {
        console.warn('Unexpected response status:', responseData);
        setSubmissionStatus('error');
        setErrors({ 
          general: { 
            type: 'error',
            title: 'Unexpected Error',
            errors: { message: 'Unexpected response from server' }
          } 
        });
        setIsErrorPopupOpen(true);
      }
    } catch (error) {
      console.error('Error:', error);
      setSubmissionStatus('error');
      setErrors({ 
        general: { 
          type: 'error',
          title: 'Error',
          errors: { message: error.message }
        } 
      });
      setIsErrorPopupOpen(true);
    }

    console.groupEnd();
    setOutput(jsonData);
  };

  const renderFormInputs = (type) => (
    <motion.div
      className="form-inputs"
      initial={{ opacity: 0, x: -30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h3 className="section-title">Details</h3>
      <input
        type="text"
        placeholder="LG Name"
        value={FormData[type].lgName}
        onChange={(e) => handleInputChange(e, type, "lgName")}
        className={`input-field ${errors?.formValidation?.errors?.lgName ? 'input-error' : ''}`}
      />
      <input
        type="email"
        placeholder="Email"
        value={FormData[type].email}
        onChange={(e) => handleInputChange(e, type, "email")}
        className={`input-field ${errors?.formValidation?.errors?.email ? 'input-error' : ''}`}
      />

      <span className="phone-prefix">+62</span>
      <input
        type="tel"
        placeholder="Phone Number"
        value={FormData[type].phone}
        onChange={(e) => handleInputChange(e, type, "phone")}
        className={`input-field ${errors?.formValidation?.errors?.phone ? 'input-error' : ''}`}
      />
    </motion.div>
  );

  const ErrorPopup = ({ errors, status, onClose }) => {
    const [expandedSections, setExpandedSections] = useState({});
    const [showAllRecords, setShowAllRecords] = useState({});

    const toggleSection = (sectionKey) => {
      setExpandedSections(prev => ({
        ...prev,
        [sectionKey]: !prev[sectionKey]
      }));
    };

    const toggleShowAll = (sectionKey) => {
      setShowAllRecords(prev => ({
        ...prev,
        [sectionKey]: !prev[sectionKey]
      }));
    };

    const getErrorTypeColor = (errorType) => {
      switch (errorType) {
        case 'validation_error':
          return '#dc3545';
        case 'partial_success':
          return '#ffc107';
        case 'success':
          return '#28a745';
        default:
          return '#6c757d';
      }
    };

    const renderErrorSection = (key, value) => {
      const errorItems = Object.entries(value.errors || {});
      const showAll = showAllRecords[key];
      const displayItems = showAll ? errorItems : errorItems.slice(0, 5);
      const hasMore = errorItems.length > 5;

      return (
        <div key={key} className="error-section">
          <div className="error-section-header" onClick={() => toggleSection(key)}>
            <h3 style={{ color: getErrorTypeColor(value.type) }}>
              {value.title || key}
              {value.type !== 'success' && <span className="error-count">({errorItems.length} items)</span>}
            </h3>
            <span className="toggle-icon">{expandedSections[key] ? '▼' : '▶'}</span>
          </div>
          {expandedSections[key] && (
            <div className="error-section-content">
              {displayItems.map(([field, error], index) => (
                <div key={index} className="field-error">
                  <div className="field-header">
                    <span className="field-name">{field}</span>
                    {field.includes('record_') && (
                      <span className="record-number">
                        Record #{field.split('_').pop()}
                      </span>
                    )}
                  </div>
                  <div className="error-message">
                    {typeof error === 'object' ? JSON.stringify(error) : error}
                  </div>
                </div>
              ))}
              {hasMore && !showAll && (
                <button 
                  className="show-more-button"
                  onClick={() => toggleShowAll(key)}
                >
                  Show {errorItems.length - 5} more items
                </button>
              )}
              {hasMore && showAll && (
                <button 
                  className="show-less-button"
                  onClick={() => toggleShowAll(key)}
                >
                  Show less
                </button>
              )}
            </div>
          )}
        </div>
      );
    };

    if (status === 'success') {
      return (
        <div className="success-popup">
          <div className="success-icon">✓</div>
          <h2>Success!</h2>
          <p>{errors?.success?.errors?.message || 'Your data has been submitted successfully.'}</p>
          <button className="action-button" onClick={onClose}>Close</button>
        </div>
      );
    }

    return (
      <div className="error-popup-content">
        <div className="error-popup-header">
          <h2>Submission Results</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <div className="error-popup-body">
          {Object.entries(errors).map(([key, value]) => renderErrorSection(key, value))}
        </div>
        <div className="error-popup-footer">
          <button className="action-button" onClick={onClose}>Close</button>
        </div>
      </div>
    );
  };

  return (
    <motion.div
      className="form-container horizontal-form"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="form-section">
        <h2 className="section-title">Select Status</h2>
        <div className="dropdowns">
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setSelectedProvince("");
              setSelectedKabupaten("");
              setKabupatenList([]);
            }}
            className={`select-status small-select ${errors?.formValidation?.errors?.status ? 'input-error' : ''}`}
          >
            <option value="">-- Select --</option>
            <option value="provincial">Provincial</option>
            <option value="kabupaten">Kabupaten</option>
          </select>

          {status && (
            <select
              value={selectedProvince}
              onChange={handleProvinceChange}
              className={`select-status small-select ${errors?.formValidation?.errors?.province ? 'input-error' : ''}`}
            >
              <option value="">-- Select Province --</option>
              {provinces.map((prov) => (
                <option key={prov.adm_code} value={prov.LG}>
                  {prov.LG}
                </option>
              ))}
            </select>
          )}

          {status === "kabupaten" && (
            <select
              value={selectedKabupaten}
              onChange={(e) => setSelectedKabupaten(e.target.value)}
              className={`select-status small-select ${errors?.formValidation?.errors?.kabupaten ? 'input-error' : ''}`}
              disabled={!kabupatenList.length}
            >
              <option value="">-- Select Kabupaten --</option>
              {kabupatenList.map((kab) => (
                <option key={kab.adm_code} value={kab.LG}>
                  {kab.LG}
                </option>
              ))}
            </select>
          )}
        </div>
        {status && renderFormInputs(status)}
      </div>

      <div className="form-section">
        <h3 className="section-title">Upload Excel Files</h3>
        <div className="file-upload-grid">
          {Object.keys(files).map((key) => (
            <div key={key} className="file-upload-card">
              <div className="file-content">
                {!files[key] ? (
                  <>
                    <label className="file-label">
                      <span className="upload-icon">+</span>
                      <span className="file-title">{key}</span>
                      <input
                        type="file"
                        accept=".xls,.xlsx"
                        onChange={(e) => handleFileChange(e, key)}
                        className="hidden-input"
                      />
                    </label>
                    <p className="file-instruction">Click to upload</p>
                  </>
                ) : (
                  <div className="file-preview">
                    <div className="file-info">
                      <span className="file-name">{files[key].name}</span>
                      <button
                        className="remove-btn"
                        onClick={() => removeFile(key)}
                      >
                        ×
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
        <button onClick={handleSubmit} className="button-submit">
          Generate Report
        </button>

        {output && (
          <div className="output-box">
            <pre>{JSON.stringify(output, null, 2)}</pre>
          </div>
        )}
      </div>

      {errors && isErrorPopupOpen && (
        <div className="error-popup-overlay" onClick={() => setIsErrorPopupOpen(false)}>
          <div className="error-popup-content" onClick={(e) => e.stopPropagation()}>
            <ErrorPopup 
              errors={errors} 
              status={submissionStatus} 
              onClose={() => setIsErrorPopupOpen(false)} 
            />
          </div>
        </div>
      )}
    </motion.div>
  );
}

export default Form;