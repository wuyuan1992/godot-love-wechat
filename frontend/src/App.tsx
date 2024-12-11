import { useEffect, useState } from "react";
import logo from "./assets/logo.png";
import SettingsDialog, { ISettings } from "./components/SettingDIalog";
function App() {
  const [, setSettings] = useState<ISettings>();
  useEffect(() => {
    const getSettings = () => {
      window.pywebview.api.get_settings().then((values) => {
        console.log(values);
        // @ts-expect-error this is a python value
        setSettings(values);
      });
    };
    if (window.pywebview) {
      getSettings();
    } else {
      window.addEventListener("pywebviewready", getSettings);
    }
    return () => {
      window.removeEventListener("pywebviewready", getSettings);
    };
  }, []);
  return (
    <div className="w-full h-full bg-gray-100">
      <nav className="flex items-center justify-between bg-white p-4 shadow-md">
        <div className="logo">
          <img src={logo} alt="logo" className="h-12"></img>
        </div>
        <div className="text-center flex-grow">
          <span>项目</span>
        </div>
        <div className="settigns">
          <SettingsDialog
            setSettings={(values) => {
              setSettings(values);
            }}
          ></SettingsDialog>
        </div>
      </nav>
    </div>
  );
}

export default App;
