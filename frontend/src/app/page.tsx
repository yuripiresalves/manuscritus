"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { AuthorsNumber } from "@/components/authors-number";
import { Models } from "@/components/models";
import { useToast } from "@/hooks/use-toast";

interface RequestData {
  num_authors: number;
  models: string[];
}

interface ResponseData {
  accuracy_svm?: number;
  accuracy_svm_grid_search?: number;
  best_params_svm?: Record<string, string | number>;
  accuracy_rf?: number;
  confusion_matrix?: number[][];
  error: number;
}

const getResultsFromApi = async (data: RequestData) => {
  const response = await fetch("http://localhost:8000/results", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const responseData: ResponseData = await response.json();
  return responseData;
};

export default function Home() {
  const [numAuthors, setNumAuthors] = useState(20);
  const [models, setModels] = useState<Record<string, boolean>>({
    svm: false,
    random_forest: false,
    knn: false,
    decision_tree: false,
    naive_bayes: false,
  });
  const [response, setResponse] = useState<ResponseData | null>(null);
  const [loading, setLoading] = useState(false);

  const { toast } = useToast();

  const handleSubmit = async () => {
    if (Object.values(models).every((value) => !value)) {
      toast({
        title: "Erro",
        description: "Selecione ao menos um modelo para análise.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    const requestData = {
      num_authors: numAuthors,
      models: Object.entries(models)
        .filter(([, value]) => value)
        .map(([key]) => key),
    };

    try {
      const result = await getResultsFromApi(requestData);
      setResponse(result);
    } catch (error) {
      console.error("Error:", error);
      setResponse({ error: -1 });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>Manuscritus</CardTitle>
          <p className="text-gray-500">
            Ferramenta baseada em caractrísticas grafométricas para a
            identificação de manuscritos.
          </p>
        </CardHeader>

        <CardContent className="space-y-6">
          <p className="text-gray-500">
            Ajuste o número de autores e selecione os modelos específicos para
            análise. Após definir as configurações, clique em
            <span className="font-bold"> Obter resultados</span> para visualizar
            a acurácia de cada modelo.
          </p>
          <AuthorsNumber
            numAuthors={numAuthors}
            setNumAuthors={setNumAuthors}
          />

          <Models models={models} setModels={setModels} />

          <Button onClick={handleSubmit} disabled={loading} className="w-full">
            {loading ? (
              <p className="flex items-center gap-2">
                <span className="size-4 border-2 border-t-2 border-neutral-50 border-t-neutral-900 rounded-full animate-spin"></span>
                carregando
              </p>
            ) : (
              "Obter resultados"
            )}
          </Button>
        </CardContent>

        {response && (
          <CardFooter className="flex flex-col">
            <div className="w-full">
              {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <Skeleton className="h-28" />
                  <Skeleton className="h-28" />
                  <Skeleton className="h-28" />
                </div>
              ) : response.error !== -1 ? (
                <>
                  <h3 className="text-lg font-semibold mb-4">Acurácia:</h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {response.accuracy_svm && (
                      <Card className="bg-gray-100">
                        <CardContent className="p-4">
                          <h4 className="text-sm font-medium text-gray-500 mb-2">
                            SVM
                          </h4>
                          <p className="text-4xl font-bold text-primary">
                            {response.accuracy_svm.toFixed(2)}%
                          </p>
                        </CardContent>
                      </Card>
                    )}
                    {response.accuracy_svm_grid_search && (
                      <Card className="bg-gray-100">
                        <CardContent className="p-4">
                          <h4 className="text-sm font-medium text-gray-500 mb-2">
                            SVM (Grid Search)
                          </h4>
                          <p className="text-4xl font-bold text-primary">
                            {response.accuracy_svm_grid_search.toFixed(2)}%
                          </p>
                        </CardContent>
                      </Card>
                    )}
                    {response.accuracy_rf && (
                      <Card className="bg-gray-100">
                        <CardContent className="p-4">
                          <h4 className="text-sm font-medium text-gray-500 mb-2">
                            Random Forest
                          </h4>
                          <p className="text-4xl font-bold text-primary">
                            {response.accuracy_rf.toFixed(2)}%
                          </p>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                  <div>
                    {/* {response.confusion_matrix && (
                      <div className="w-full mt-8">
                        <h3 className="text-lg font-semibold mb-4">
                          Matriz de confusão:
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {response.confusion_matrix.map((row, i) => (
                            <Card key={i} className="bg-gray-100">
                              <CardContent className="p-4">
                                <h4 className="text-sm font-medium text-gray-500 mb-2">
                                  Classe {i}
                                </h4>
                                <div className="grid grid-cols-3 gap-2">
                                  {row.map((value, j) => (
                                    <p key={j} className="text-center">
                                      {value}
                                    </p>
                                  ))}
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </div>
                    )} */}
                    {response.best_params_svm && (
                      <div className="w-full mt-8">
                        <h3 className="text-lg font-semibold mb-4">
                          Melhores parâmetros (SVM):
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {Object.entries(response.best_params_svm).map(
                            ([key, value]) => (
                              <Card key={key} className="bg-gray-100">
                                <CardContent className="p-4">
                                  <h4 className="text-sm font-medium text-gray-500 mb-2">
                                    {key}
                                  </h4>
                                  <p className="text-4xl font-bold text-primary">
                                    {value}
                                  </p>
                                </CardContent>
                              </Card>
                            )
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </>
              ) : response.error === -1 ? (
                <p className="text-red-500">
                  Ocorreu um erro ao buscar os dados.
                </p>
              ) : (
                <p className="text-gray-500">Nenhuma resposta ainda</p>
              )}
            </div>
          </CardFooter>
        )}
      </Card>
    </div>
  );
}
