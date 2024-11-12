import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";

interface ModelsProps {
  models: Record<string, boolean>;
  setModels: (value: Record<string, boolean>) => void;
}

export function Models({ models, setModels }: ModelsProps) {
  const availableModels = [
    { key: "svm", label: "SVM" },
    { key: "random_forest", label: "Random Forest" },
    // { key: "knn", label: "KNN" },
    // { key: "decision_tree", label: "Árvore de Decisão" },
    // { key: "naive_bayes", label: "Naive Bayes" },
  ];

  return (
    <div className="space-y-2">
      <Label>Modelos</Label>
      <div className="flex flex-col gap-4">
        {availableModels.map((model) => (
          <div key={model.key} className="flex items-center space-x-2">
            <Checkbox
              id={model.key}
              checked={models[model.key]}
              onCheckedChange={(checked) =>
                setModels({ ...models, [model.key]: checked as boolean })
              }
            />
            <Label className="cursor-pointer" htmlFor={model.key}>
              {model.label}
            </Label>
          </div>
        ))}
      </div>
    </div>
  );
}
