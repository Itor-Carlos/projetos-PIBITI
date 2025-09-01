import Image from "next/image";

export default function Home() {
  return (
    <div>
      <h1>Welcome to the Home Page</h1>
      <Image
        src="/path/to/image.jpg"
        alt="Description of image"
        width={500}
        height={500}
      />
    </div>
  );
}
