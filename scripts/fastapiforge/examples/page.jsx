import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { usePathname } from 'next/navigation'


export default function Page() {
	const [getCards, setCards] = useState([]);
	const router = useRouter();
	const path = usePathname(); // path atual
	
	useEffect(() => {
		// Main
		example()
	},[])

	function example() {
		console.log("Example function");
	};

	return(
		<>
			<a>{path}<a/>
		</>
	)
}