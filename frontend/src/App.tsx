import logo from "./assets/logo.png";
import { Button } from "./components/ui/button";
import { Settings } from "lucide-react";
import { Dialog } from "./components/ui/dialog";
import { DialogTrigger } from "@radix-ui/react-dialog";
import SettingsDialog from "./components/SettingDIalog";
function App() {
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
          <Dialog>
            <DialogTrigger>
              <Button variant="outline" size="icon">
                <Settings />
              </Button>
            </DialogTrigger>
            <SettingsDialog></SettingsDialog>
          </Dialog>
        </div>
      </nav>
    </div>
  );
}

export default App;
