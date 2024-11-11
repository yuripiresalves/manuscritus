import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";

interface AuthorsNumberProps {
  numAuthors: number;
  setNumAuthors: (value: number) => void;
}

export function AuthorsNumber({
  numAuthors,
  setNumAuthors,
}: AuthorsNumberProps) {
  const handleNumAuthorsChange = (value: number | string) => {
    setNumAuthors(Number(value));
  };

  const handleSliderChange = (value: number[]) => {
    setNumAuthors(value[0]);
  };

  return (
    <>
      <div className="space-y-2">
        <Label htmlFor="num-authors">Número de Autores</Label>
        <p
          id="num-authors-description"
          className="text-sm text-muted-foreground"
        >
          Escolha um valor entre 20 e 200.
        </p>
      </div>
      <div className="flex items-center space-x-4">
        <Input
          id="num-authors"
          type="number"
          min={20}
          max={200}
          step={20}
          value={numAuthors}
          // disabled
          onChange={(e) => handleNumAuthorsChange(e.target.value)}
          className="w-24"
          aria-describedby="num-authors-description"
        />
        <Slider
          value={[numAuthors]}
          onValueChange={handleSliderChange}
          min={20}
          max={200}
          step={20}
          className="flex-grow"
        />
      </div>
    </>
  );
}
