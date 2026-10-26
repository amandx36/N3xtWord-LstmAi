
import Header from "./component/header";
import MiddlePart from "./component/middlePart";
import Footer from "./component/footer";

export default function Home() {
  return (
    <>
      <Header />
      <main>
        <MiddlePart />
      </main>
      <Footer />
    </>
  );
}