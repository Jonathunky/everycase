import { useMDXComponents } from "../../../mdx-components";

const Wrapper = useMDXComponents().wrapper;

export const generateStaticParams = async () => {
  return [];
};

export async function generateMetadata() {
  return {
    title: "Custom Markdown Page",
    description: "A simple custom Markdown page.",
  };
}

export default async function Page(props) {
  const params = await props.params;

  // Example table of contents (if applicable)
  const toc = [];

  // Example metadata
  const metadata = {
    title: "Custom Page",
  };

  // Log the full URL path
  console.log("Current page URL:", `/case/${params.model}`);

  return (
    <Wrapper toc={toc} metadata={metadata}>
      {/* Output the URL path as the title */}
      <h1 className="_mt-2 _text-4xl _font-bold _tracking-tight _text-slate-900 dark:_text-slate-100">{`/case/${params.model}`}</h1>
      # this should be the title
    </Wrapper>
  );
}
