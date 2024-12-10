import { SubmitHandler, useForm } from "react-hook-form";
import {
  DialogHeader,
  DialogContent,
  DialogTitle,
  DialogFooter,
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
import { Folder } from "lucide-react";

interface ISettings {
  godotExecute: string;
}

const SettingsDialog = () => {
  const form = useForm<ISettings>();
  const onSubmit: SubmitHandler<ISettings> = (data) => console.log(data);

  return (
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
                    <Button variant="outline" size="icon">
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
  );
};

export default SettingsDialog;
