import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";

import App from "../src/App";

test("welcome screen renders", () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <App />
    </QueryClientProvider>,
  );
  expect(screen.getByText("Ask for a clear technical resolution.")).toBeInTheDocument();
});
