import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";

import { Button } from "@/components/ui/button";
import { ArrowRightToLine, Settings } from "lucide-react";

export interface Project {
  name: string;
  description: string;
  version: string;
  icon: string;
}

export interface ProjectCardProps extends Project {
  key: number;
}

const ProjectCard = (props: ProjectCardProps) => {
  return (
    <Card key={props.key}>
      <CardHeader className="flex items-center space-x-3">
        <img
          src={`data:image/jpeg;base64,${props.icon}`}
          width={64}
          height={64}
        ></img>
        <CardTitle>{props.name}</CardTitle>
        <CardDescription>{props.description}</CardDescription>
        <CardDescription>Version:{props.version}</CardDescription>
        <CardContent className="mt-4">
          <div className="flex justify-between">
            <Button variant="outline" size="icon">
              <ArrowRightToLine />
            </Button>
            <Button variant="outline" size="icon">
              <Settings />
            </Button>
          </div>
        </CardContent>
      </CardHeader>
    </Card>
  );
};

export default ProjectCard;
