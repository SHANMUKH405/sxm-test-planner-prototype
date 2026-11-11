import CatalogueClient from "./catalogue-client";
import { api } from "@/lib/api";

export default async function CataloguePage() {
  const tests = await api.catalogue();
  return <><header className="pageHead"><div><div className="eyebrow">Robot repository</div><h1>Test catalogue</h1><p className="subtitle">Every card is an existing Robot test. Product logic remains in the `.robot` file; the application provides discovery and orchestration.</p></div></header><CatalogueClient initial={tests}/></>;
}
