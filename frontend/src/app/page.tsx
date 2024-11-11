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

interface RequestData {
  num_authors: number;
  models: string[];
}

// Simulated API call
const mockApiCall = async (data: RequestData) => {
  const response = await fetch("http://localhost:8000/results", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const responseData = await response.json();
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
  const [response, setResponse] = useState<Record<string, number> | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    const requestData = {
      num_authors: numAuthors,
      models: Object.entries(models)
        .filter(([, value]) => value)
        .map(([key]) => key),
    };

    try {
      const result = await mockApiCall(requestData);
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
        </CardHeader>

        <CardContent className="space-y-6">
          <p className="text-gray-500">
            Você pode ajustar o número de autores e selecionar os modelos
            específicos para análise. Após definir as configurações, clique em
            <span className="font-bold"> Obter resultados</span> para visualizar
            a acurácia de cada modelo modelo.
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
          <CardFooter>
            <div className="w-full">
              <h3 className="text-lg font-semibold mb-4">Acurácia:</h3>
              {loading ? (
                //skeleton card
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <Skeleton className="h-28" />
                  <Skeleton className="h-28" />
                  <Skeleton className="h-28" />
                </div>
              ) : response.error !== -1 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(response).map(([key, value]) => (
                    <Card key={key} className="bg-gray-100">
                      <CardContent className="p-4">
                        <h4 className="text-sm font-medium text-gray-500 mb-2">
                          {key === "accuracy_svm" && "SVM"}
                          {key === "accuracy_svm_grid_search" &&
                            "SVM (Busca em Grade)"}
                          {key === "accuracy_rf" && "Floresta Aleatória"}
                          {key === "accuracy_knn" && "KNN"}
                          {key === "accuracy_decision_tree" &&
                            "Árvore de Decisão"}
                          {key === "accuracy_naive_bayes" && "Naive Bayes"}
                        </h4>
                        <p className="text-4xl font-bold text-primary">
                          {value.toFixed(2)}%
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
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
