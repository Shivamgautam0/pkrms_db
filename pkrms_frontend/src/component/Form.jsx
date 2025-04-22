import React, { useState, useEffect, useCallback, useRef } from "react";
import * as XLSX from "xlsx";
import "../css/Form.css";
import { fetchProvinceList, filterKabupatenList } from "../Services/services";
import { motion } from "framer-motion";

/**
 * Form Component
 * Handles user inputs, file uploads, and data submission for road infrastructure data
 */
function Form() {
  // ======== STATE MANAGEMENT ========

  // Form selection states
  const [status, setStatus] = useState(""); // Provincial or Kabupaten selection
  const [selectedProvince, setSelectedProvince] = useState("");
  const [selectedKabupaten, setSelectedKabupaten] = useState("");
  const [provinces, setProvinces] = useState([]);
  const [kabupatenList, setKabupatenList] = useState([]);


  // File management states
  const [files, setFiles] = useState({});
  const [excelJson, setExcelJson] = useState({});
  // Add near your other state declarations
  const [uploadingSections, setUploadingSections] = useState({});
  // Form submission states
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [output, setOutput] = useState(null);
  const [errors, setErrors] = useState({});
  const [isErrorPopupOpen, setIsErrorPopupOpen] = useState(false);
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [popupMessages, setPopupMessages] = useState([]);
  // Track which sections have been uploaded
  const [uploadedSections, setUploadedSections] = useState({});

  // Active section state
  const [activeSection, setActiveSection] = useState(null);

  // Form data state
  const [FormData, setFormData] = useState({
    provincial: { lgName: "", email: "", phone: "" },
    kabupaten: { lgName: "", email: "", phone: "" },
  });

  /**
   * Maps technical file names to user-friendly display names
   * @param {String} technicalName - The original technical file name
   * @returns {String} - User-friendly display name
   */
  const getDisplayName = (technicalName) => {
    const displayNameMap = {
      CODE_AN_UnitCostsPER: "PER",
      CODE_AN_UnitCostsPERUnpaved: "PER Unpaved",
      CODE_AN_UnitCostsREH: "REH",
      CODE_AN_UnitCostsRIGID: "RIGID",
      CODE_AN_UnitCostsRM: "RM",
      CODE_AN_UnitCostsUPGUnpaved: "UPG Unpaved",
      CODE_AN_UnitCostsWidening: "Widening",
      CODE_AN_UnitCostsStandard: "Standard",
      CODE_AN_Parameters: "Parameters",
      CODE_AN_WidthStandards: "Width Standards",
      // Add other mappings as needed
    };

    return displayNameMap[technicalName] || technicalName;
  };
  // Section configuration state - defines all file upload sections
  const [sections, setSections] = useState({
    unitCosts: {
      label: "Unit Cost Section",
      files: [
        "CODE_AN_UnitCostsPER",
        "CODE_AN_UnitCostsPERUnpaved",
        "CODE_AN_UnitCostsREH",
        "CODE_AN_UnitCostsRIGID",
        "CODE_AN_UnitCostsRM",
        "CODE_AN_UnitCostsUPGUnpaved",
        "CODE_AN_UnitCostsWidening",
      ],
      enabled: true,
      required: true,
    },
    parameters: {
      label: "Parameters & Traffic",
      files: [
        "CODE_AN_Parameters",
        "CODE_AN_WidthStandards",
        "TrafficWeightingFactors",
      ],
      enabled: true,
      required: true,
    },
    map: {
      label: "Links",
      files: [
        { name: "Link", enabled: true, required: true },
        { name: "Alignment", enabled: false, required: false },
        { name: "DRP", enabled: false, required: false },
      ],
      enabled: true,
      required: true,
    },
    survey: {
      label: "Survey",
      files: [
        { name: "RoadInventory", enabled: false, required: true },
        { name: "RoadCondition", enabled: false, required: false },
        { name: "RoadHazard", enabled: false, required: false },
      ],
      enabled: false,
      required: true,
    },
  });

  // Define structure and traffic sections at the top level
  const [structureFiles] = useState([
    "CulvertInventory",
    "RetainingWallInventory",
    "CulvertCondition",
    "RetainingWallCondition",
    "BridgeInventory",
  ]);

  const [trafficFiles] = useState(["TrafficVolume"]);

  const [uploadedData, setUploadedData] = useState({});

  // ======== EFFECTS ========

  /**
   * Load provinces list on component mount
   */
  useEffect(() => {
    setProvinces(fetchProvinceList());
  }, []);

  /**
   * Manage section availability based on completed uploads
   * - Structure section becomes available when Survey is complete
   * - Traffic section becomes available when Structure is complete
   */
  useEffect(() => {
    const unitCostsComplete = sections.unitCosts.files.every((fileKey) =>
      typeof fileKey === "string" ? files[fileKey] : files[fileKey.name]
    );

    const parametersComplete = sections.parameters.files.every((fileKey) =>
      typeof fileKey === "string" ? files[fileKey] : files[fileKey.name]
    );

    const linkUploaded = !!files["Link"];

    setSections((prev) => ({
      ...prev,
      map: { ...prev.map, enabled: true },
      survey: { ...prev.survey, enabled: linkUploaded },
    }));
  }, [files]);

  /**
   * Update file enablement based on file uploads
   * - Link section: Enable Alignment and DRP when Link is uploaded
   * - Survey section: Enable Road Condition and Road Hazard when Road Inventory is uploaded
   */
  // Update this useEffect to check for successful Link upload
  useEffect(() => {
    // Handle Link section dependencies
    setSections(prev => {
      // This checks if Link exists AND was successfully uploaded
      const linkSuccessfullyUploaded = !!files['Link'] && uploadedSections['map'];

      const updatedMapFiles = prev.map.files.map(file => {
        if (typeof file === 'object') {
          if (file.name === 'Link') {
            // Link is always enabled
            return { ...file, enabled: true };
          } else {
            // Other files like Alignment and DRP are only enabled if Link was successfully uploaded
            return { ...file, enabled: linkSuccessfullyUploaded };
          }
        }
        return file;
      });

      return {
        ...prev,
        map: {
          ...prev.map,
          files: updatedMapFiles
        },
        // Survey section is also enabled only after Link was successfully uploaded
        survey: {
          ...prev.survey,
          enabled: linkSuccessfullyUploaded
        }
      };
    });
  }, [files, uploadedSections]); // Added uploadedSections to dependencies

  // ======== EVENT HANDLERS ========

  /**
   * Handles province selection change
   * Updates the kabupaten list based on selected province
   */
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

  /**
   * Updates form data fields when user inputs values
   * @param {Object} e - Event object
   * @param {String} type - Form type (provincial or kabupaten)
   * @param {String} field - Field name to update
   */
  const handleInputChange = useCallback((e, type, field) => {
    const value = e.target.value;
    setFormData((prev) => ({
      ...prev,
      [type]: { ...prev[type], [field]: value },
    }));
  }, []);

  const prevSectionsRef = useRef(sections);

  // Effect to handle section disable and file cleanup
  useEffect(() => {
    const prevSections = prevSectionsRef.current;

    // Check each section for disable transitions
    Object.entries(sections).forEach(([sectionKey, currentSection]) => {
      const prevSection = prevSections[sectionKey];

      // If section was enabled and is now disabled
      if (prevSection?.enabled && !currentSection.enabled) {
        // Extract all file keys from the section
        const filesToRemove = currentSection.files.map((file) =>
          typeof file === "string" ? file : file.name
        );

        // Remove files from state
        setFiles((prevFiles) => {
          const newFiles = { ...prevFiles };
          filesToRemove.forEach((fileKey) => delete newFiles[fileKey]);
          return newFiles;
        });

        setExcelJson((prevExcel) => {
          const newExcel = { ...prevExcel };
          filesToRemove.forEach((fileKey) => delete newExcel[fileKey]);
          return newExcel;
        });
      }
    });

    // Update previous sections reference
    prevSectionsRef.current = sections;
  }, [sections]); // Trigger when sections change

  /**
   * Handles file uploads and processes Excel files
   * @param {Object} e - Event object
   * @param {String} key - File identifier
   */
  const handleFileChange = useCallback(
    async (e, key) => {
      const file = e.target.files[0];
      if (!file) return;

      // Check if trying to upload DRP or Alignment without Link being successfully uploaded
      if ((key === "DRP" || key === "Alignment") && !uploadedSections["map"]) {
        setPopupMessages(["Please upload and process the Link section first"]);
        setIsErrorPopupOpen(true);
        e.target.value = ""; // Clear the file input
        return;
      }

      // Additional check for DRP and Alignment files
      if ((key === "DRP" || key === "Alignment") && !files["Link"]) {
        setPopupMessages(["Please upload the Link file first"]);
        setIsErrorPopupOpen(true);
        e.target.value = ""; // Clear the file input
        return;
      }

      // Validate file extension
      const validExtensions = [".xls", ".xlsx"];
      const fileExtension = file.name.split(".").pop().toLowerCase();

      if (!validExtensions.includes(`.${fileExtension}`)) {
        setPopupMessages(["Only Excel files (.xls, .xlsx) are allowed"]);
        setIsErrorPopupOpen(true);
        e.target.value = ""; // Clear the file input
        return;
      }

      try {
        // Read and process Excel file
        const data = await file.arrayBuffer();
        const workbook = XLSX.read(data, { type: "buffer" });

        // Process all sheets in the workbook
        const allData = {};
        workbook.SheetNames.forEach((sheetName) => {
          const jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
          // Convert to array of records
          allData[sheetName] = jsonData;
        });

        // Store file reference and processed data
        const firstSheetName = workbook.SheetNames[0];
        setFiles((prev) => {
          if (prev[key]?.name === file.name) return prev; // Prevent update if same file
          return { ...prev, [key]: file };
        });
        setExcelJson((prev) => ({
          ...prev,
          [key]: allData[firstSheetName], // This now contains an array of records
        }));
      } catch (error) {
        setPopupMessages([
          "Error reading Excel file. Please check the file format.",
        ]);
        setIsErrorPopupOpen(true);
        console.error(error);
      }
    },
    [uploadedSections, files]
  );

  /**
   * Removes a file from the state
   * @param {String} key - File identifier to remove
   */
  const dependencyMap = {
    Link: ["Alignment", "DRP"],
    RoadInventory: ["RoadCondition", "RoadHazard"],
  };

  // Update the removeFile function to handle dependent files
  const removeFile = useCallback((key) => {
    setFiles((prev) => {
      const updatedFiles = { ...prev };

      // Remove the specified file and its dependencies
      const removeFileAndDependencies = (fileKey) => {
        delete updatedFiles[fileKey];
        // Remove dependent files recursively
        if (dependencyMap[fileKey]) {
          dependencyMap[fileKey].forEach((dependentKey) => {
            removeFileAndDependencies(dependentKey);
          });
        }
      };

      removeFileAndDependencies(key);
      return updatedFiles;
    });

    setExcelJson((prev) => {
      const updated = { ...prev };
      const removeDataAndDependencies = (fileKey) => {
        delete updated[fileKey];
        if (dependencyMap[fileKey]) {
          dependencyMap[fileKey].forEach((dependentKey) => {
            removeDataAndDependencies(dependentKey);
          });
        }
      };

      removeDataAndDependencies(key);
      return updated;
    });

    // Update section enablement states
    setSections((prev) => {
      const newSections = { ...prev };

      // Handle Link dependencies
      if (key === "Link") {
        newSections.map.files = prev.map.files.map((file) =>
          typeof file === "object" ? { ...file, enabled: false } : file
        );
        newSections.map.files[0].enabled = true; // Keep Link enabled
      }

      // Handle Road Inventory dependencies
      if (key === "RoadInventory") {
        newSections.survey.files = prev.survey.files.map((file) =>
          typeof file === "object" ? { ...file, enabled: false } : file
        );
        newSections.survey.files[0].enabled = true; // Keep Road Inventory enabled
      }

      return newSections;
    });
  }, []);

  // Update the useEffect for file dependencies
  useEffect(() => {
    // Handle Link section dependencies
    setSections((prev) => {
      const linkExists = !!files["Link"];
      const updatedMapFiles = prev.map.files.map((file) => {
        if (typeof file === "object") {
          return {
            ...file,
            enabled: file.name === "Link" ? true : linkExists,
          };
        }
        return file;
      });

      return {
        ...prev,
        map: {
          ...prev.map,
          files: updatedMapFiles,
        },
      };
    });

    // Handle Survey section dependencies
    setSections((prev) => {
      const roadInventoryExists = !!files["RoadInventory"];
      const updatedSurveyFiles = prev.survey.files.map((file) => {
        if (typeof file === "object") {
          return {
            ...file,
            enabled: file.name === "RoadInventory" ? true : roadInventoryExists,
          };
        }
        return file;
      });

      return {
        ...prev,
        survey: {
          ...prev.survey,
          files: updatedSurveyFiles,
        },
      };
    });
  }, [files]);

  /**
   * Handles section-specific file upload to backend
   * @param {String} sectionKey - Key of the section to upload
   */
  const handleSectionUpload = async (sectionKey) => {
    console.log("Starting section upload for:", sectionKey);
    const section = sections[sectionKey];
    if (!section) {
      console.error("Section not found:", sectionKey);
      return;
    }
  
    // Validate form inputs first
    if (!validateInputs()) return;
    if (isSubmitting) return;
    setUploadingSections(prev => ({
      ...prev,
      [sectionKey]: true
    }));
  
    setIsSubmitting(true);
  
    // Get all required files for this section
    const requiredFiles = section.files
      .filter((file) => {
        if (typeof file === "string") return true;
        return file.required;
      })
      .map((file) => (typeof file === "string" ? file : file.name));
  
    console.log("Required files:", requiredFiles);
    console.log("Current files state:", files);
  
    // Check if all required files are present
    const missingFiles = requiredFiles.filter((fileKey) => !files[fileKey]);
    if (missingFiles.length > 0) {
      console.log("Missing required files:", missingFiles);
  
      setErrors({
        unitCosts: {
          type: "validation_error",
          title: `${section.label} Missing Files`,
          errors: {
            missingFiles: `Please upload all required files: ${missingFiles.join(", ")}`,
          },
        },
      });
      setSubmissionStatus("error");
      setIsErrorPopupOpen(true);
      setIsSubmitting(false);
      setUploadingSections(prev => ({
        ...prev,
        [sectionKey]: false
      }));
      return;
    }
  
    try {
      // Format phone number with prefix
      const prependPrefix = (phone) => {
        if (!phone) return "";
        return phone.startsWith("+62")
          ? phone
          : `+62${phone.replace(/^0+/, "")}`;
      };
  
      // Get province and kabupaten codes
      const provinceObj = provinces.find((p) => p.LG === selectedProvince);
      if (!provinceObj) {
        console.error("Province not found:", selectedProvince);
        setPopupMessages(["Please select a valid province"]);
        setIsErrorPopupOpen(true);
        setIsSubmitting(false);
        setUploadingSections(prev => ({
          ...prev,
          [sectionKey]: false
        }));
        return;
      }
  
      // Prepare form data with province code
      const currentFormData = FormData[status];
      const preparedFormData = {
        status: status,
        admin_code: provinceObj.adm_prov + "00", // Combine province code with default kabupaten code
        lg_name: currentFormData.lgName,
        email: currentFormData.email,
        phone: prependPrefix(currentFormData.phone),
      };
  
      // Handle kabupaten case
      if (status === "kabupaten") {
        const kabupatenObj = kabupatenList.find(
          (k) => k.LG === selectedKabupaten
        );
        if (!kabupatenObj) {
          console.error("Kabupaten not found:", selectedKabupaten);
          setPopupMessages(["Please select a valid kabupaten"]);
          setIsErrorPopupOpen(true);
          setIsSubmitting(false);
          setUploadingSections(prev => ({
            ...prev,
            [sectionKey]: false
          }));
          return;
        }
        preparedFormData.admin_code =
          provinceObj.adm_prov + kabupatenObj.adm_kab; // Combine province and kabupaten codes
      }
  
      // Prepare data for this section
      const sectionData = {
        FormData: [preparedFormData],
      };
  
      // Add all files from this section (both required and optional)  
      let allSectionFiles = section.files.map((file) =>
        typeof file === "string" ? file : file.name
      );
  
      if (sectionKey === "survey") {
        allSectionFiles = [
          ...allSectionFiles,
          ...structureFiles,
          ...trafficFiles,
        ];
      }
  
      // Check if this is a Link upload or DRP/Alignment upload
      const isLinkUpload =
        sectionKey === "map" && files["Link"] && !uploadedSections["map"];
      const isDRPOrAlignmentUpload =
        sectionKey === "map" && (files["DRP"] || files["Alignment"]) && uploadedSections["map"];
      const isRoadInventoryUpload =
        sectionKey === "survey" && files["RoadInventory"] && !uploadedSections["survey"];
  
      if (isLinkUpload) {
        // For Link upload, only send the Link file
        if (excelJson["Link"]) {
          sectionData["Link"] = excelJson["Link"];
        }
      } else if (isDRPOrAlignmentUpload) {
        // For DRP/Alignment upload, send only those files
        if (files["DRP"] && excelJson["DRP"]) {
          sectionData["DRP"] = excelJson["DRP"];
        }
        if (files["Alignment"] && excelJson["Alignment"]) {
          sectionData["Alignment"] = excelJson["Alignment"];
        }
      } else if (isRoadInventoryUpload) {
        // For RoadInventory upload, only send the RoadInventory file
        if (excelJson["RoadInventory"]) {
          sectionData["RoadInventory"] = excelJson["RoadInventory"];
        }
        // Also include RoadCondition if it exists
        if (excelJson["RoadCondition"]) {
          sectionData["RoadCondition"] = excelJson["RoadCondition"];
        }
        // Also include RoadHazard if it exists
        if (excelJson["RoadHazard"]) {
          sectionData["RoadHazard"] = excelJson["RoadHazard"];
        }
      } else {
        // For all other cases, process files normally
        allSectionFiles.forEach((fileKey) => {
          if (excelJson[fileKey]) {
            sectionData[fileKey] = excelJson[fileKey];
          }
        });
      }
  
      console.log("Sending data to backend:", sectionData);
  
      // Make API request
      const response = await fetch("http://127.0.0.1:8000/api/upload-data/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(sectionData),
      });
  
      const responseData = await response.json();
      console.log("Backend response:", responseData);
  
      if (!response.ok) {
        // Handle validation errors
        if (
          responseData.status === "validation_error" ||
          responseData.status === "error"
        ) {
          let formattedErrors = {};
  
          // Handle FormData validation errors
          if (responseData.errors?.FormData_record_2?.errors) {
            formattedErrors.FormData = {
              type: "validation_error",
              title: "Form Errors",
              errors: {},
            };
            const formErrors = responseData.errors.FormData_record_2.errors;
            Object.entries(formErrors).forEach(([field, error]) => {
              let errorMessage = error;
              if (field === "admin_code") {
                errorMessage =
                  status === "provincial"
                    ? "Please select a valid province"
                    : "Please select a valid kabupaten";
              } else if (field === "lg_name") {
                errorMessage = "Please enter a valid local government name";
              } else if (field === "email") {
                errorMessage = "Please enter a valid email address";
              } else if (field === "phone") {
                errorMessage =
                  "Please enter a valid phone number (9-14 digits)";
              }
              formattedErrors.FormData.errors[field] = errorMessage;
            });
          }
  
          // Handle file-specific errors
          if (responseData.errors) {
            Object.entries(responseData.errors).forEach(
              ([key, errorDetails]) => {
                if (key !== "FormData_record_2") {
                  const [fileName, recordNumber] = key.includes("_")
                    ? key.split("_")
                    : [key, "N/A"];
  
                  // Convert file names to user-friendly names
                  const friendlyFileName = fileName
                    .replace("CODE_AN_", "")
                    .replace(/([A-Z])/g, " $1")
                    .trim();
  
                  if (errorDetails.errors) {
                    formattedErrors[friendlyFileName] = {
                      type: "validation_error",
                      title: `${friendlyFileName} Errors`,
                      errors: {},
                    };
  
                    const errorText = Array.isArray(errorDetails.errors)
                      ? errorDetails.errors.join(", ")
                      : Object.entries(errorDetails.errors)
                        .map(([field, errors]) => {
                          const friendlyField = field
                            .replace(/_/g, " ")
                            .replace(/\b\w/g, (l) => l.toUpperCase());
                          return `${friendlyField}: ${Array.isArray(errors) ? errors.join(", ") : errors
                            }`;
                        })
                        .join("; ");
  
                    formattedErrors[friendlyFileName].errors[
                      `Record ${recordNumber}`
                    ] = errorText;
                  } else if (errorDetails.message) {
                    if (
                      errorDetails.message.includes("doesn't have a") &&
                      errorDetails.message.includes("model")
                    ) {
                      formattedErrors[friendlyFileName] = {
                        type: "error",
                        title: "Model Error",
                        errors: {
                          message: `The system is not configured to handle ${friendlyFileName} data yet. Please contact support.`,
                        },
                      };
                    } else {
                      formattedErrors[friendlyFileName] = {
                        type: "error",
                        title: "Error",
                        errors: { message: errorDetails.message },
                      };
                    }
                  }
                }
              }
            );
          }
  
          setErrors(formattedErrors);
          setSubmissionStatus("error");
          setIsErrorPopupOpen(true);
          
          // THIS IS THE KEY CHANGE - Only remove the tick indicator for this section 
          // if it's a Link upload or a regular section, but not for DRP/Alignment uploads
          if (!isDRPOrAlignmentUpload) {
            setUploadedSections((prev) => ({
              ...prev,
              [sectionKey]: false,
            }));
          } 
          // For DRP/Alignment uploads with errors, we keep the "map" section marked as uploaded
          
          setIsSubmitting(false);
          setUploadingSections(prev => ({
            ...prev,
            [sectionKey]: false
          }));
          return;
        }
  
        throw new Error(
          responseData.message || `HTTP error! status: ${response.status}`
        );
      }
  
      // Handle success response
      if (responseData.status === "success") {
        setSubmissionStatus("success");
        setErrors({
          success: {
            type: "success",
            title: "Success",
            errors: {
              message: responseData.message || "Data uploaded successfully",
            },
          },
        });
        setIsErrorPopupOpen(true);
        setUploadedData(prev => ({
          ...prev,
          [sectionKey]: sectionData
        }));
        
        // Set the tick indicator for this section
        // For DRP/Alignment uploads, we don't modify the "map" section's uploaded status
        // For RoadInventory uploads, we don't modify the "survey" section's uploaded status
        if (!isDRPOrAlignmentUpload && !isRoadInventoryUpload) {
          setUploadedSections((prev) => ({
            ...prev,
            [sectionKey]: true,
          }));
        }
  
        // Enable dependent sections only if Link section was successfully uploaded
        if (sectionKey === "map" && !isDRPOrAlignmentUpload) {
          const linkUploaded = files["Link"];
          setSections((prev) => ({
            ...prev,
            map: {
              ...prev.map,
              files: prev.map.files.map((file) => {
                if (
                  typeof file === "object" &&
                  (file.name === "Alignment" || file.name === "DRP")
                ) {
                  return { ...file, enabled: linkUploaded };
                }
                return file;
              }),
            },
            survey: {
              ...prev.survey,
              enabled: linkUploaded,
            },
          }));
        }
      } else if (responseData.status === "partial_success") {
        setSubmissionStatus("partial_success");
        const formattedErrors = {};
  
        // Format successful models
        if (
          responseData.successful_models &&
          responseData.successful_models.length > 0
        ) {
          formattedErrors.successful_models = {
            type: "success",
            title: "Successfully Processed Models",
            errors: {},
          };
          responseData.successful_models.forEach((model) => {
            formattedErrors.successful_models.errors[model] =
              "Successfully processed";
          });
        }
  
        // Format error details
        if (responseData.errors) {
          Object.entries(responseData.errors).forEach(([model, records]) => {
            formattedErrors[model] = {
              type: "validation_error",
              title: `${model} Errors`,
              errors: {},
            };
  
            Object.entries(records).forEach(([recordKey, errorData]) => {
              const recordNumber = recordKey.split("_").pop();
              const errorMessage = Array.isArray(errorData.errors)
              ? errorData.errors.join(", ")
              : Object.entries(errorData.errors)
                  .map(([field, errors]) => {
                    if (field === "__all__") {
                      return Array.isArray(errors) ? errors.join(", ") : errors;
                    }
                    return `${field}: ${Array.isArray(errors) ? errors.join(", ") : errors}`;
                  })
                  .join("; ");
            
                         
  
              formattedErrors[model].errors[`Record ${recordNumber}`] =
                errorMessage;
            });
          });
        }
  
        setErrors(formattedErrors);
        setIsErrorPopupOpen(true);
        
        // Same logic for partial success - don't remove map section status for DRP/Alignment uploads
        // and don't remove survey section status for RoadInventory uploads
        if (!isDRPOrAlignmentUpload && !isRoadInventoryUpload) {
          setUploadedSections((prev) => ({
            ...prev,
            [sectionKey]: false,
          }));
  
          // Disable dependent sections if Link section upload failed
          if (sectionKey === "map") {
            setSections((prev) => ({
              ...prev,
              map: {
                ...prev.map,
                files: prev.map.files.map((file) => {
                  if (
                    typeof file === "object" &&
                    (file.name === "Alignment" || file.name === "DRP")
                  ) {
                    return { ...file, enabled: false };
                  }
                  return file;
                }),
              },
              survey: {
                ...prev.survey,
                enabled: false,
              },
            }));
          }
        }
      }
    } catch (error) {
      console.error("Upload error:", error);
      setErrors({
        general: {
          type: "error",
          title: "Upload Error",
          errors: { message: error.message },
        },
      });
      setSubmissionStatus("error");
      setIsErrorPopupOpen(true);
      
      // Same logic for exception handling - don't remove map section status for DRP/Alignment uploads
      // and don't remove survey section status for RoadInventory uploads
      if (!(sectionKey === "map" && (files["DRP"] || files["Alignment"]) && uploadedSections["map"]) &&
          !(sectionKey === "survey" && files["RoadInventory"] && uploadedSections["survey"])) {
        setUploadedSections((prev) => ({
          ...prev,
          [sectionKey]: false,
        }));
      }
    } finally {
      setIsSubmitting(false);
      setUploadingSections(prev => ({
        ...prev,
        [sectionKey]: false
      }));
    }
  };

  /**
   * Validates form inputs before submission
   * @returns {Boolean} - Whether all inputs are valid
   */
  const validateInputs = () => {
    const errors = {};

    if (!status) {
      errors.status = "Status is required";
    }

    if (!selectedProvince) {
      errors.province = "Province is required";
    }

    if (status === "kabupaten" && !selectedKabupaten) {
      errors.kabupaten = "Kabupaten is required";
    }

    const { lgName, email, phone } = FormData[status] || {};

    if (!lgName?.trim()) {
      errors.lgName = "LG Name is required";
    }

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
      errors.email = "Please enter a valid email address";
    }

    const phoneRegex = /^[0-9]{9,14}$/;
    if (!phoneRegex.test(phone?.replace(/^\+62/, ""))) {
      errors.phone = "Phone number must be 9 to 14 digits";
    }
    if (Object.keys(errors).length > 0) {
      setErrors({
        formValidation: {
          title: "Form Validation Errors",
          errors: errors,
        },
      });
      setIsErrorPopupOpen(true);
      return false;
    }

    return true;
  };

  /**
   * Handles section button click
   * @param {String} sectionKey - Key of the section to activate
   */
  const handleSectionClick = (sectionKey) => {
    const section = sections[sectionKey];

    if (!section.enabled) {
      const message =
        sectionMessages[sectionKey] || "This section is currently disabled";

      setErrors({
        general: {
          type: "section_error",
          title: "Section Access Error",
          errors: { [sectionKey]: message },
        },
      });
      setSubmissionStatus("error");
      setIsErrorPopupOpen(true);
      return;
    }

    setActiveSection(activeSection === sectionKey ? null : sectionKey);
  };

  /**
   * Closes the active section
   */
  const handleCloseSection = () => {
    setActiveSection(null);
  };

  // ======== RENDERING HELPER FUNCTIONS ========

  /**
   * Renders file upload cards for a specific section
   * @param {Array} fileList - List of files to render
   * @param {Boolean} usesObjectFormat - Whether files are stored as objects with name and enabled properties
   * @returns {JSX.Element} - File upload cards UI
   */
  const renderFileUploadCards = (fileList, usesObjectFormat = false) => {
    return (
      <div className="file-upload-grid">
        {fileList.map((fileItem) => {
          // Handle both string and object file formats
          const key = usesObjectFormat ? fileItem.name : fileItem;
          const isEnabled = usesObjectFormat ? fileItem.enabled : true;
          const isRequired = usesObjectFormat ? fileItem.required : false;

          // Get user-friendly display name while keeping original key for functionality
          const displayName = getDisplayName(key);

          // Additional check for DRP and Alignment files
          const isDRPOrAlignment = key === "DRP" || key === "Alignment";
          const isLinkUploaded = files["Link"] && uploadedSections["map"];
          const shouldDisable = isDRPOrAlignment && !isLinkUploaded;

          return (
            <div
              key={key}
              className={`file-upload-card ${!isEnabled || shouldDisable ? "disabled" : ""
                }`}
            >
              <div className="file-content">
                {!files[key] ? (
                  <label
                    className={`file-label ${!isEnabled || shouldDisable ? "disabled" : ""
                      }`}
                  >
                    <div className="upload-content">
                      <span className="upload-icon">+</span>
                      <span className="file-title">
                        {displayName}
                        {isRequired && (
                          <span className="required-indicator">*</span>
                        )}
                      </span>
                      <p className="file-instruction">
                        {shouldDisable
                          ? "Upload Link section first"
                          : !isEnabled
                            ? "Upload prerequisite files first"
                            : "Click to upload"}
                      </p>
                    </div>
                    <input
                      type="file"
                      accept="application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                      onChange={(e) => handleFileChange(e, key)}
                      className="hidden-input"
                      id={`file-input-${key}`}
                      disabled={!isEnabled || shouldDisable}
                    />
                  </label>
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
          );
        })}
      </div>
    );
  };

  /**
   * Renders active section content
   * @returns {JSX.Element} - Active section UI
   */
  const renderActiveSection = () => {
    if (!activeSection) return null;
  
    const section = sections[activeSection];
    const isUploaded = uploadedSections[activeSection];
    
    // Determine if there are any files uploaded for this section
    let hasRequiredFiles = false;
    
    if (activeSection === "survey") {
      const allSurveyFiles = [
        ...section.files.map((file) => (typeof file === "string" ? file : file.name)),
        ...structureFiles,
        ...trafficFiles,
      ];
      hasRequiredFiles = allSurveyFiles.some((fileKey) => files[fileKey]);
    } else if (activeSection === "map" || activeSection === "unitCosts" || activeSection === "parameters") {
      // For other sections, check if any required files exist
      hasRequiredFiles = section.files.some((file) => {
        const fileKey = typeof file === "string" ? file : file.name;
        return files[fileKey];
      });
    }
  
    return (
      <motion.div
        className="active-section-container"
        initial={{ opacity: 0, height: 0 }}
        animate={{ opacity: 1, height: "auto" }}
        exit={{ opacity: 0, height: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="section-header">
          <h3 className="active-section-title">{section.label}</h3>
          <button className="section-close-button" onClick={handleCloseSection}>
            ×
          </button>
        </div>
  
        {/* Render main section file upload cards */}
        {renderFileUploadCards(
          section.files,
          activeSection === "map" || activeSection === "survey"
        )}
  
        {/* Survey-specific subsections */}
        {activeSection === "survey" && (
          <>
            <div className="subsection-container">
              <h4 className="subsection-title">Structure</h4>
              {renderFileUploadCards(structureFiles)}
            </div>
            <div className="subsection-container">
              <h4 className="subsection-title">Traffic</h4>
              {renderFileUploadCards(trafficFiles)}
            </div>
          </>
        )}
        
        {/* Upload button for ALL sections */}
        <div className="section-upload-container">
          <button
            className={`section-upload-button ${isUploaded ? 'uploaded' : ''} ${uploadingSections[activeSection] ? 'uploading' : ''}`}
            onClick={() => handleSectionUpload(activeSection)}
            disabled={!hasRequiredFiles || uploadingSections[activeSection]}
          >
            {uploadingSections[activeSection] ? 'Uploading...' : (isUploaded ? '✓ Re-upload Section' : 'Upload Section')}
          </button>
        </div>{uploadedData[activeSection] && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <h4 className="data-preview-title">Uploaded Data Preview</h4>
          <DataTable data={uploadedData[activeSection]} />
        </motion.div>
      )}
    </motion.div>
    );
  };

  /**
   * Renders form input fields
   * @param {String} type - Form type (provincial or kabupaten)
   * @returns {JSX.Element} - Form inputs UI
   */
  const renderFormInputs = (type) => (
    <motion.div
      className="form-inputs"
      initial={{ opacity: 0, x: -30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h3 className="section-title">Details</h3>
      <label htmlFor="lgname">LG Name </label>
      <input
        id="lgname"
        type="text"
        placeholder="Enter LG Name"
        value={FormData[type].lgName}
        onChange={(e) => handleInputChange(e, type, "lgName")}
        className="input-field"
      />
      <label htmlFor="email">Email </label>
      <input
        id="email"
        type="email"
        placeholder="Enter Email Address"
        value={FormData[type].email}
        onChange={(e) => handleInputChange(e, type, "email")}
        className="input-field"
      />
      <label htmlFor="phone">Phone </label>
      <span className="phone-prefix">+62</span>
      <input
        id="phone"
        type="tel"
        placeholder="Enter Phone Number"
        value={FormData[type].phone}
        onChange={(e) => handleInputChange(e, type, "phone")}
        className="input-field"
      />
    </motion.div>
  );

  /**
   * Calculate progress for each section
   * @param {String} sectionKey - Key of the section
   * @returns {Number} - Progress percentage
   */
  const calculateSectionProgress = (sectionKey) => {
    const section = sections[sectionKey];
    if (!section) return 0;

    // Calculate total files
    let totalFiles = 0;
    let uploadedFiles = 0;

    // Count enabled files in sections with objects
    if (sectionKey === "map" || sectionKey === "survey") {
      const enabledFiles = section.files.filter((file) => file.enabled);
      totalFiles = enabledFiles.length;
      uploadedFiles = enabledFiles.filter((file) => files[file.name]).length;
    } else {
      // Original counting for simple string arrays
      totalFiles = section.files.length;
      uploadedFiles = section.files.filter((key) => files[key]).length;
    }

    // Add structure files to the count for survey section
    if (sectionKey === "survey") {
      totalFiles += structureFiles.length;
      uploadedFiles += structureFiles.filter((key) => files[key]).length;
      totalFiles += trafficFiles.length;
      uploadedFiles += trafficFiles.filter((key) => files[key]).length;

    }

    return totalFiles > 0 ? Math.round((uploadedFiles / totalFiles) * 100) : 0;
  };

  /**
   * Get the count of files uploaded out of the total available files
   * @param {String} sectionKey - Key of the section
   * @returns {Object} - Object with uploaded and total counts
   */
  const getSectionFileCounts = (sectionKey) => {
    const section = sections[sectionKey];
    if (!section) return { uploaded: 0, total: 0 };

    let uploaded = 0;
    let total = 0;

    // For sections with objects
    if (sectionKey === "map" || sectionKey === "survey") {
      const enabledFiles = section.files.filter((file) => file.enabled);
      total = enabledFiles.length;
      uploaded = enabledFiles.filter((file) => files[file.name]).length;
    } else {
      // Original counting for simple string arrays
      total = section.files.length;
      uploaded = section.files.filter((key) => files[key]).length;
    }

    // Add structure counts for survey section
    if (sectionKey === "survey") {
      const structureUploaded = structureFiles.filter((key) => files[key]).length;
      const trafficUploaded = trafficFiles.filter((key) => files[key]).length;

      return {
        uploaded,
        total,
        structureUploaded,
        structureTotal: structureFiles.length,
        trafficUploaded,
        trafficTotal: trafficFiles.length,
      };

    }

    return { uploaded, total };
  };

  /**
   * Error display component
   */
  const ErrorDisplay = ({ errors, status, onClose }) => {
    const [expandedSections, setExpandedSections] = useState({});
    const [showAllRecords, setShowAllRecords] = useState({});

    const toggleSection = (sectionKey) => {
      setExpandedSections((prev) => ({
        ...prev,
        [sectionKey]: !prev[sectionKey],
      }));
    };

    const toggleShowAll = (sectionKey) => {
      setShowAllRecords((prev) => ({
        ...prev,
        [sectionKey]: !prev[sectionKey],
      }));
    };

    const getErrorTypeColor = (errorType) => {
      switch (errorType) {
        case "validation_error":
          return "#dc3545";
        case "partial_success":
          return "#ffc107";
        case "success":
          return "#28a745";
        default:
          return "#6c757d";
      }
    };

    const renderErrorSection = (key, value) => {
      const errorItems = Object.entries(value.errors || {});
      const showAll = showAllRecords[key];
      const displayItems = showAll ? errorItems : errorItems.slice(0, 5);
      const hasMore = errorItems.length > 5;

      return (
        <div key={key} className="error-section">
          <div
            className="error-section-header"
            onClick={() => toggleSection(key)}
          >
            <h3 style={{ color: getErrorTypeColor(value.type) }}>
              {value.title || key}
              {value.type !== "success" && (
                <span className="error-count">({errorItems.length} items)</span>
              )}
            </h3>
            <span className="toggle-icon">
              {expandedSections[key] ? "▼" : "▶"}
            </span>
          </div>
          {expandedSections[key] && (
            <div className="error-section-content">
              {displayItems.map(([field, error], index) => (
                <div key={index} className="field-error">
                  <div className="field-header">
                    <span className="field-name">{field}</span>
                    {field.includes("record_") && (
                      <span className="record-number">
                        Record #{field.split("_").pop()}
                      </span>
                    )}
                  </div>
                  <div className="error-message">
                    {typeof error === "object" ? JSON.stringify(error) : error}
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

    if (status === "success") {
      return (
        <div className="success-message">
          <div className="success-icon">✓</div>
          <h2>Success!</h2>
          <p>
            {errors?.success?.errors?.message ||
              "Your data has been submitted successfully."}
          </p>
          <button 
        className="action-button" 
        onClick={() => {
          onClose();
          // Optionally scroll to the data preview
        }}
      >
        View Data
      </button>
        </div>
      );
    }

    return (
      <div className="error-display">
        <div className="error-display-header">
          <h2>Submission Results</h2>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="error-display-body">
          {Object.entries(errors).map(([key, value]) =>
            renderErrorSection(key, value)
          )}
        </div>
        <div className="error-display-footer">
          <button className="action-button" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    );
  };
  // ======== MAIN COMPONENT RENDER ========
  return (
    <motion.div
      className="form-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Left Form Section - Status and Details */}
      <div className="form-section">
        <h2 className="section-title">Select Status</h2>
        <div className="dropdowns">
          {/* Status Selection */}
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setSelectedProvince("");
              setSelectedKabupaten("");
              setKabupatenList([]);
            }}
            className={`select-status small-select ${errors?.formValidation?.errors?.status ? "input-error" : ""
              }`}
          >
            <option value="">-- Select --</option>
            <option value="provincial">Provincial</option>
            <option value="kabupaten">Kabupaten</option>
          </select>

          {/* Province Selection */}
          {status && (
            <select
              value={selectedProvince}
              onChange={handleProvinceChange}
              className={`select-status small-select ${errors?.formValidation?.errors?.province ? "input-error" : ""
                }`}
            >
              <option value="">-- Select Province --</option>
              {provinces.map((prov) => (
                <option key={prov.adm_code} value={prov.LG}>
                  {prov.LG}
                </option>
              ))}
            </select>
          )}

          {/* Kabupaten Selection */}
          {status === "kabupaten" && (
            <select
              value={selectedKabupaten}
              onChange={(e) => setSelectedKabupaten(e.target.value)}
              className={`select-status small-select ${errors?.formValidation?.errors?.kabupaten ? "input-error" : ""
                }`}
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

        {/* Form Inputs */}
        {status && renderFormInputs(status)}
      </div>

      {/* Section Buttons Grid */}
      <div className="form-section">
        <h3 className="section-title">Upload Excel Files</h3>
        <div className="section-buttons-grid">
          {Object.entries(sections).map(([sectionKey, section]) => {
            const fileCounts = getSectionFileCounts(sectionKey);
            const isUploaded = uploadedSections[sectionKey];
            return (
              <motion.button
                key={sectionKey}
                className={`section-button ${!section.enabled ? "disabled" : ""
                  } ${activeSection === sectionKey ? "active" : ""}`}
                onClick={() => handleSectionClick(sectionKey)}
                disabled={!section.enabled}
                whileHover={section.enabled ? { scale: 1.03 } : {}}
                whileTap={section.enabled ? { scale: 0.97 } : {}}
              >
                <div className="section-button-content">
                  <span className="section-label">{section.label}</span>
                  {section.required && (
                    <span className="required-badge">*</span>
                  )}
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${calculateSectionProgress(sectionKey)}%`,
                      }}
                    ></div>
                  </div>
                  <span className="progress-text">
                    {fileCounts.uploaded}/{fileCounts.total} files
                    {sectionKey === "survey" &&
                      ` + ${fileCounts.structureUploaded}/${fileCounts.structureTotal} structure` +
                      ` + ${fileCounts.trafficUploaded}/${fileCounts.trafficTotal} traffic`}

                  </span>
                  {isUploaded && (
                    <div className="uploaded-badge">
                      <span className="tick-icon">✓</span>
                    </div>
                  )}
                </div>
              </motion.button>
            );
          })}
        </div>

        {/* Active Section File Uploads */}
        {renderActiveSection()}

        {/* Error Popup */}
        {errors && isErrorPopupOpen && (
          <div className="error-display-container">
            <ErrorDisplay
              errors={errors}
              status={submissionStatus}
              onClose={() => setIsErrorPopupOpen(false)}
            />
          </div>
        )}
      </div>
    </motion.div>

    
  );
}
const DataTable = ({ data }) => {
  if (!data) return null;

  return (
    <div className="data-table-container">
      {Object.entries(data).map(([fileName, fileData]) => (
        <div key={fileName} className="file-table-section">
          <h4 className="table-title">{fileName}</h4>
          <div className="table-scroll-container">
            <table className="data-table">
              <thead>
                <tr>
                  {fileData.length > 0 &&
                    Object.keys(fileData[0]).map((header) => (
                      <th key={header}>{header}</th>
                    ))}
                </tr>
              </thead>
              <tbody>
                {fileData.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, i) => (
                      <td key={i}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
};


export default Form;
