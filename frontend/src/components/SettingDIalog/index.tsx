import { SubmitHandler, useForm } from "react-hook-form";
import {
  DialogHeader,
  DialogContent,
  DialogTitle,
  DialogFooter,
  DialogTrigger,
  Dialog,
} from "../ui/dialog";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
} from "../ui/form";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { Folder, Settings } from "lucide-react";
import { useEffect, useState } from "react";

export interface ISettings {
  godotExecute: string;
}

interface DialogProps {
  setSettings: (value: ISettings) => void;
}

const SettingsDialog = (props: DialogProps) => {
  const form = useForm<ISettings>({});
  const [open, setOpen] = useState(false);
  const onSubmit: SubmitHandler<ISettings> = (data) => {
    window.pywebview.api.save_settings(data).then(() => {
      props.setSettings(data);
      setOpen(false);
    });
  };
  const { setValue } = form;

  useEffect(() => {
    const getToolsSettings = () => {
      window.pywebview.api.get_settings().then((values) => {
        // @ts-expect-error this is a python value
        setValue("godotExecute", values.godotExecute);
      });
    };
    if (window.pywebview) {
      getToolsSettings();
    } else {
      window.addEventListener("pywebviewready", getToolsSettings);
    }
    return () => {
      window.removeEventListener("pywebviewready", getToolsSettings);
    };
  }, [setValue]);

  const getExecuteGodot = () => {
    window.pywebview.api.get_godot_execute().then((value) => {
      setValue("godotExecute", String(value), { shouldValidate: true });
      setOpen(true);
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="icon">
          <Settings />
        </Button>
      </DialogTrigger>
      <DialogContent className="w-96">
        <DialogHeader>
          <DialogTitle>工具设置</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
              control={form.control}
              name="godotExecute"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Godot执行文件</FormLabel>
                  <FormControl>
                    <div className="flex w-full max-w-sm items-center space-x-1">
                      <Input placeholder="C:\godot.exe" {...field} />
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => {
                          getExecuteGodot();
                        }}
                      >
                        <Folder />
                      </Button>
                    </div>
                  </FormControl>
                  <FormDescription>
                    选择Godot执行文件地址，用来导出游戏资源包
                  </FormDescription>
                </FormItem>
              )}
            ></FormField>
            <DialogFooter>
              <Button type="submit">保存</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
};

export default SettingsDialog;
