// Lógica para a página do catálogo

const products = [
        { id: 1, name: "Camiseta Básica", price: "R$ 324,90", img: "static/images/CamisaBrancaCTRZ.jpg", category: "Camisetas", url: "static/details/CamisetaBrancaCTRZ.html" },
        { id: 2, name: "Jorts Cortez", price: "R$ 1990,00", img: "/static/images/BermudaCTRZ.jpg", category: "Calças/Bermudas", url: "static/details/JortsCTRZ.html" },
        { id: 3, name: "Casaco Cortez", price: "R$ 749,90", img: "/static/images/CasacoAmareloCTRZ.jpg", category: "Casacos/Jaquetas", url: "static/details/CasacoAmareloCTRZ.html" },
        { id: 4, name: "Jaqueta de Couro Cortez", price: "R$ 2400,00", img: "/static/images/JaquetaPreta1CTRZ.jpg", category: "Casacos/Jaquetas", url: "static/details/JaquetaCouroCTRZ.html" },
        { id: 5, name: "AirMax 95 x Cortez", price: "R$ 7500,00", img: "/static/images/AirMax95CTRZ1.jpg", category: "Calçados", url: "static/details/AirMax95.html" },
        { id: 6, name: "Calça Cargo", price: "R$ 1300,00", img: "/static/images/Calça1CTRZ.jpg", category: "Calças/Bermudas", url: "static/details/CalçaCargoCTRZ.html" },
        { id: 7, name: "Casaco Azul", price: "R$ 900,00", img: "/static/images/CasacoAzulCTRZ.jpg", category: "Casacos/Jaquetas", url: "static/details/CasacoAzulCTRZ.html" },
        { id: 8, name: "Calça EWCRUEL", price: "R$ 800,00", img: "/static/images/CalçaEWCRUEL.jpg", category: "Calças/Bermudas", url: "static/details/CalçaCRUEL.html" },
        { id: 9, name: "Fleece Class", price: "R$ 750,00", img: "/static/images/FleeceCLASS.jpg", category: "Casacos/Jaquetas", url: "static/details/FleeceCLASS.html" },
        { id: 10, name: "Camiseta de Time", price: "R$ 2200,00", img: "/static/images/CamisaAmarelaCTRZ.jpg", category: "Camisetas", url: "static/details/CamisetaTimeCTRZ.html" },
    ];
        
        
    const renderCatalog = (category = "all") => {
        const catalog = document.getElementById("catalog");
        catalog.innerHTML = ""; // Limpa o catálogo
    
        // Filtra os produtos com base na categoria
        const filteredProducts = category === "all" 
            ? products 
            : products.filter(product => product.category === category);
        
        // Criação do card para cada produto
        filteredProducts.forEach(product => {
            const productCard = document.createElement("div");
            productCard.classList.add("product-card");
    
            // Aqui geramos o conteúdo do cartão de cada produto, com link
            productCard.innerHTML = `
                <a href="${product.url}" class="product-link">
                    <img src="${product.img}" alt="${product.name}">
                </a>
                <h3>${product.name}</h3>
                <p class="price">${product.price}</p>
            `;
            
            // Adiciona o card do produto no catálogo
            catalog.appendChild(productCard);
        });
    };
    
    // Configurar botões de categoria
    document.querySelectorAll(".category-btn").forEach(button => {
        button.addEventListener("click", (e) => {
            const category = e.target.getAttribute("data-category");
            document.querySelectorAll(".category-btn").forEach(btn => btn.classList.remove("active"));
            e.target.classList.add("active");
            renderCatalog(category);
        });
    });
    
    // Carregar catálogo inicialmente
    renderCatalog();
