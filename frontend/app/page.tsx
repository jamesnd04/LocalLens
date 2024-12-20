import LandingLogo from "@/assets/LandingLogo.svg";
import Image from "next/image";



export default function Home() {
  return (
    
    <div className="flex flex-col justify-center items-center">
      <div className="flex flex-col w-full gap-20 items-center">
      <Image src={LandingLogo} alt="Landing Logo" width={500} height={500}/>
        <div
          className="container"
          style={{ maxWidth: "800px", margin: "0 auto" }}
        >
          <div
            className="grid"
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "20px",
            }}
          >
            <div
              className="card"
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "20px",
              }}
            >
              <div className="content" style={{ marginBottom: "10px" }}>
                <p className="font-bold text-lg ">Immerse as a Local.</p>
                <p className="color-black">
                  Immerse yourself in the local cultures and niches wherever you are.
                  With collaboration from locals, we provide you with the authentic cultures and experiences of your current
                  location. No more of the same tourist spots and franchises. Get to truly know your surroundings like a native.
                </p>
              </div>
            </div>
            <div
              className="card"
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "20px",
              }}
            >
              <div className="content" style={{ marginBottom: "10px" }}>
                <p className="font-bold text-lg">
                  Personalized for You.
                </p>
                <p>
                  We provide you with a personalized experience based on your interests and preferences. 
                  With our AI Agent, we can recommend you the best places to visit, the best food to eat, and the best activities to do based on your preferences.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  );
}

