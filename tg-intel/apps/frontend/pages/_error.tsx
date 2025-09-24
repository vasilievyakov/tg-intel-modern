import NextErrorComponent, { ErrorProps } from "next/error";

function ErrorPage(props: ErrorProps) {
  return <NextErrorComponent statusCode={props.statusCode} />;
}

ErrorPage.getInitialProps = async (ctx: any) => {
  const errorProps = await (NextErrorComponent as any).getInitialProps(ctx);
  return { ...errorProps };
};

export default ErrorPage;


