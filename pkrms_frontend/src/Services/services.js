import jsonfile from '../Services/balaiLGMapping.json'; 


export const fetchProvinceList = () => {
    const data = jsonfile.filter((item) => item.adm_type.trim() === "P");
    return data;
  };
  export const fetchKabupatenList = () => {
    const data = jsonfile.filter((item) => item.adm_type === "K");
    return data;
  };
  
  export const filterKabupatenList = (provinceCode) => {
    const data = jsonfile.filter(
      (item) => item.adm_type === "K" && item.adm_prov === parseInt(provinceCode)
    );
    return data;
  };