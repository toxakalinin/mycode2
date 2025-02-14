/* Основной фон и анимация */
body {
    background: linear-gradient(120deg, #000103, #131339, #00001a);
    background-size: 300% 300%;
    animation: backgroundAnimation 10s ease infinite;
    color: #e0e0e0;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    text-align: center;
    margin: 0;
    padding: 0;
}

@keyframes backgroundAnimation {
    0% {
        background-position: 0% 50%;
    }
 
    50% {
        background-position: 100% 50%;
    }
 
    100% {
        background-position: 0% 50%;
    }
}

 /* Нижнее меню (фиксированное внизу экрана) */
 footer .bottom-menu {
     display: flex;
     justify-content: space-around;
     position: fixed;
     width: 100%;                                                                                
     bottom: 0;                                                                                  
     opacity: 0.85;                                                                              
     transition: opacity 0.5s ease;                                                              
     z-index: 1000;                                                                              
 }                                                                                               
                                                                                                 
 footer .menu-item {                                                                             
     display: flex;                                                                              
     flex-direction: column;                                                                     
     align-items: center;                                                                        
     background-color: #002141;                                                                      
     text-decoration: none;                                                                      
     color: #131339;                                                                             
     padding-right: 10px;                                                                        
     width: 80px;                                                                                
 }                                                                                               
                                                                                                 
 footer .menu-item img {                                                                         
     width: 90px;                                                                                
     height: 80px;                                                                               
     margin-bottom: 0px;                                                                         
     border: 1px solid #00ffff;                                                                  
     border-radius: 11px;                                                                        
     box-shadow: 0 10px 17px rgba(0, 0, 0, 0.5);                                                 
                                                                                                 
}                                                                                                 

footer .menu-item span {                                                                        
     font-size: 3vw;                                                                             
}                                                                                               
                                                                                                 
footer .menu-item:hover {                                                                       
     background-color: #180032;                                                                  
     border-radius: 10px;                                                                        
     transition: background-color 0.8s ease;                                                    
}                                                                                               
                                                                                                 
 /* Футер в конце страницы */                                                                    
.page-footer {                                                                                  
     background-color: #111111;                                                                  
     padding: 0px;                                                                               
     text-align: center;                                                                         
     margin-top: 0px;                                                                            
     border: 2px solid #111111;                                                                      
     border-radius: 8px;                                                                         
     box-shadow: 0 8px 15px rgba(0, 0, 0, 1);                                                    
}                                                                                               
                                                                                                        
body {                                                                                                  
            margin: 0;                                                                                  
            font-family: Arial, sans-serif;                                                             
            background-color: #0c0c25;                                                                  
            color: #fff;                                                                                
            text-align: center;                                                                         
            display: flex;                                                                              
            flex-direction: column;                                                                     
            min-height: 100vh;                                                                          
        }                                                                                               
                                                                                                        
        /* Верхняя часть страницы */                                                                    
        .header-content {                                                                               
            display: flex;                                                                              
            align-items: center;                                                                        
            justify-content: center;                                                                    
            background-color: #0c0c25;                                                                  
            margin: 20px;                                                                               
            box-shadow:10px 10px 10px 10px rgba(0.5, 0.5, 0.5, 0.5);                                    
            border-radius: 7px;                                                                         
                                                                                                        
}                                                                                                       
/* Header */                                                                                            
header {                                                                                                
    text-align: center;                                                                                 
    width: 100%;                                                                                        
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);                                                           
    border: 1px solid #00ffff;                                                                          
    border-radius: 8px;                                                                                 
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);                                                          
}                                                                                                       
                                                                                                        
header h1 {                                                                                             
    font-size: 2.5em;                                                                                   
    font-family: 'Montserrat', sans-serif;                                                              
    font-weight: bold;                                                                                  
    color: #ffffff;                                                                                     
    margin: 0;                                                                                          
}                                                                                                       
                                                                                                        
.logo {                                                                                                 
    width: 80px;                                                                                        
    transition: transform 0.5s ease-in-out;                                                             
}                                                                                                       
                                                                                                        
.logo:hover {                                                                                           
    transform: rotate(360deg);                                                                          
}                                                                                                       
                                                                                                        
.content.animated-content {                                                                             
    animation: fadeInUp 1.5s ease-in-out;                                                               
}                                                                                                       
                                                                                                        
@keyframes fadeInUp {                                                                                   
    from {                                                                                              
        opacity: 0;                                                                                     
        transform: translateY(20px);                                                                    
    }                                                                                                   
                                                                                                        
    to {                                                                                                
        opacity: 1;                                                                                     
        transform: translateY(0);                                                                       
    }                                                                                                   
}                                                                                                       
                                                                                                        
/* Меню */                                                                                              
nav ul.menu {                                                                                           
    display: flex;                                                                                      
    justify-content: center;                                                                            
    gap: 10px;                                                                                          
    list-style: none;                                                                                   
}                                                                                                       
                                                                                                        
nav ul.menu li {                                                                                        
    flex: 1;                                                                                            
}                                                                                                       
                                                                                                        
nav ul.menu li a {                                                                                      
    color: #fff;                                                                                        
    box-shadow: 10px 10px 10px 10px rgba(0.3, 0.3, 0.3, 0.3);                                           
    font-weight: bold;                                                                                  
    text-decoration: none;                                                                              
    padding: 15px 25px;                                                                                 
    border-radius: 8px;                                                                                 
    background-color: #111135;                                                                          
    transition: background-color 0.3s, transform 0.3s ease-in-out, box-shadow 0.3s;                     
    display: block;                                                                                     
    text-align: center;                                                                                 
}                                                                                                       
                                                                                                        
nav ul.menu li a:hover {                                                                                
    background-color: #111135;                                                                          
    transform: translateY(-5px);                                                                        
    box-shadow: 10px 10px 10px 10px rgba(0.5, 0.5, 0.5, 0.5);                                           
}                                                                                                       
                                                                                                        
/* Основной контент */                                                                                  
.content {                                                                                              
    flex: 1;                                                                                            
    margin: 0 auto;                                                                                     
    display: flex;                                                                                      
    flex-direction: column;                                                                             
    align-items: center;                                                                                
    justify-content: center;                                                                            
}                                                                                                       
                                                                                                        
/* Приветственное сообщение */                                                                          
.content h2 {                                                                                           
    font-size: 4vw;                                                                                     
    /* Изменено на зависимость от ширины экрана */                                                      
    color: #ffffff;                                                                                     
    /* Чтобы текст переносился */                                                                       
    word-wrap: break-word;                                                                              
}                                                                                                       
                                                                                                        
/* Нижнее меню */                                                                                       
footer .bottom-menu {                                                                                   
    display: flex;                                                                                      
    justify-content: space-around;                                                                      
    align-items: center;                                                                                
    /* Добавление отступов */                                                                           
}                                                                                                       
                                                                                                        
footer .menu-item {                                                                                     
    /* Увеличение зоны клика для удобства */                                                            
    color: white;                                                                                       
    text-decoration: none;                                                                              
}                                                                                                       
                                                                                                        
/* Кнопки */                                                                                            
button {                                                                                                
    background-color: #000103;
    color: white;                                                                                       
    padding: 12px 24px;                                                                                 
    border: none;                                                                                       
    border-radius: 8px;                                                                                 
    font-size: 1.2em;                                                                                   
    cursor: pointer;                                                                                    
    transition: background-color 0.3s, transform 0.3s ease-in-out, box-shadow 0.3s;                     
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);                                                          
    width: 80%;                                                                                         
    max-width: 300px;                                                                                   
}                                                                                                       
                                                                                                        
button:hover {                                                                                          
    background-color: #131339;                                                                          
    transform: translateY(-5px);                                                                        
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);                                                         
}                                                                                                       
                                                                                                        
/* Footer footer {                                                                                      
    color: #e0e0e0;                                                                                     
    text-align: center;                                                                                 
    padding: 10px;                                                                                      
    position: fixed;                                                                                    
    bottom: 0;                                                                                          
    width: 100%;                                                                                        
    box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.2);                                                          
}*/                                                                                                     
                                                                                                        
/*footer .menu-item img {                                                                               
    width: 15px;                                                                                        
    height: 7px;                                                                                        
    margin-bottom: 5px;                                                                                 
}                                                                                                       
                                                                                                        
footer .menu-item span {                                                                                
    display: block;                                                                                     
    font-size: 12px;                                                                                    
}                                                                                                       
                                                                                                        
/* Основные стили */                                                                                    
body {                                                                                                  
    font-family: Arial, sans-serif;                                                                     
    margin: 0;                                                                                          
    padding: 0;                                                                                         
    display: flex;                                                                                      
    flex-direction: column;                                                                             
    min-height: 100vh;                                                                                  
}                                                                                                       
                                                                                                        
header {                                                                                                
    background: linear-gradient(120deg, #000103, #131339, #00001a);                                     
    color: #ffffff;                                                                                     
    text-align: center;                                                                                 
}                                                                                                       
                                                                                                        
.logo-square {                                                                                          
    width: 100px;                                                                                       
    height: 100px;                                                                                      
    display: block;                                                                                     
    margin: 0 auto;                                                                                     
}                                                                                                       
                                                                                                        
main {                                                                                                  
    flex-grow: 1;                                                                                       
    text-align: center;                                                                                 
}                                                                                                       
                                                                                                        
h2 {                                                                                                    
    margin-bottom: 20px;                                                                                
    color: #d1ecf1;                                                                                     
}                                                                                                       
                                                                                                        
p {                                                                                                     
    font-size: 18px;                                                                                    
    color: #cccccc;                                                                                     
    margin-bottom: 30px;                                                                                
}                                                                                                       
                                                                                                        
/* Основное меню */                                                                                     
.main-menu .button {                                                                                    
    display: inline-block;                                                                              
    padding: 15px 25px;                                                                                 
    margin: 10px;                                                                                       
    background-color: #00a8cc;                                                                          
    color: white;                                                                                       
    text-decoration: none;                                                                              
    font-size: 16px;                                                                                    
    border-radius: 5px;                                                                                 
    transition: background-color 0.3s ease;                                                             
}                                                                                                       
                                                                                                        
/* Футер */                                                                                             
footer {                                                                                                
    position: relative; /* Убрали фиксацию, чтобы двигался с контентом */                               
    background-color: #142850;                                                                          
    color: white;                                                                                       
    text-align: center;                                                                                 
    margin-top: auto;                                                                                   
}                                                                                                       
                                                                                                        
/* Экранные кнопки футера */                                                                            
.bottom-menu {                                                                                          
    display: flex;                                                                                      
    justify-content: space-around;                                                                      
    padding: 10px;                                                                                      
}                                                                                                       
                                                                                                        
.footer-button {                                                                                        
    color: white;                                                                                       
    text-decoration: none;                                                                              
    font-size: 14px;                                                                                    
    padding: 10px;                                                                                      
    background-color: #00a8cc;                                                                          
    border-radius: 5px;                                                                                 
    transition: background-color 0.3s ease;                                                             
}                                                                                                       
                                                                                                        
.footer-button:hover {                                                                                  
    background-color: #007a99;                                                                          
}                                                                                                       
                                                                                                        
.page-footer {                                                                                          
    width: 100%;                                                                                        
    margin-top: 20px;                                                                                   
    font-size: 12px;                                                                                    
}                                                                                                       
                                                                                                        
/* Адаптивные стили */                                                                                  
@media (max-width: 768px) {                                                                             
    .main-menu .button {                                                                                
        width: 100%;                                                                                    
        margin-bottom: 10px;                                                                            
    }                                                                                                   
                                                                                                        
    .footer-button {                                                                                    
        font-size: 12px;                                                                                
    }                                                                                                   
}                                                                                                       
                                                                                                        
/* Футер */                                                                                             
footer {                                                                                                
    position: relative; /* Убрали фиксацию, чтобы двигался с контентом */                               
    background-color: #142850;                                                                          
    color: white;                                                                                       
    text-align: center;                                                                                 
    margin-top: auto;                                                                                   
    border: 2px solid #111111;                                                                          
    border-radius: 8px;                                                                                 
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);                                                          
}                                                                                                       
                                                                                                        
/* Экранные кнопки футера */                                                                            
.bottom-menu {                                                                                          
    display: flex;                                                                                      
    justify-content: space-around;                                                                      
    width 100%;                                                                                         
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.5);                                                          
                                                                                                        
}                                                                                                       
                                                                                                        
.footer-button {                                                                                        
    color: white;                                                                                       
    text-decoration: none;                                                                              
    font-size: 14px;                                                                                    
    padding: 10px;                                                                                      
    background-color: #00a8cc;                                                                          
    border-radius: 5px;                                                                                 
    transition: background-color 0.3s ease;                                                             
}                                                                                                       
                                                                                                        
.footer-button:hover {                                                                                  
    background-color: #007a99;                                                                          
}                                                                                                       
                                                                                                        
.page-footer {                                                                                          
    margin-top: 20px;                                                                                   
    font-size: 12px;                                                                                    
}                                                                                                       
                                                                                                        
/* Адаптивные стили */                                                                                  
@media (max-width: 768px) {                                                                             
    .main-menu .button {                                                                                
        width: 100%;                                                                                    
        margin-bottom: 10px;                                                                            
    }                                                                                                   
                                                                                                        
    .footer-button {                                                                                    
        font-size: 12px;                                                                                
    }                                                                                                   
}                                                                                                       
                                                                                                        
                                                                                                        
/* Адаптивная верстка */                                                                                
@media (max-width: 1080px) {                                                                            
    h1 {                                                                                                
        font-size: 2em;                                                                                 
    }                                                                                                   
                                                                                                        
    nav ul.menu li {                                                                                    
        flex: 1 1 45%;                                                                                  
    }                                                                                                   
                                                                                                        
    button {                                                                                            
        width: 70%;                                                                                     
    }                                                                                                   
}                                                                                                       
                                                                                                        
@media (max-width: 768px) {                                                                             
    h1 {                                                                                                
        font-size: 1.8em;                                                                               
    }                                                                                                   
                                                                                                        
    nav ul.menu li {                                                                                    
        flex: 1 1 90%;                                                                                  
    }                                                                                                   
                                                                                                        
    button {                                                                                            
        font-size: 1em;                                                                                 
    }                                                                                                   
                                                                                                        
@media (max-width: 480px) {                                                                             
    h1 {                                                                                                
        font-size: 1.6em;                                                                               
    }                                                                                                   
                                                                                                        
}                                                                                                       
nav ul.menu li a {                                                                                      
        padding: 10px 15px;                                                                             
    }                                                                                                   
                                                                                                        
    button {                                                                                            
        width: 100%;                                                                                    
        font-size: 0.9em;                                                                               
        padding: 10px 20px;                                                                             
    }                                                                                                   
}                                                                                                       
/* Адаптивная верстка */                                                                                
@media (max-width: 1080px) {                                                                            
    h1 {                                                                                                
        font-size: 2em;                                                                                 
    }                                                                                                   
                                                                                                        
    nav ul.menu li {                                                                                    
        flex: 1 1 45%;                                                                                  
    }                                                                                                   
                                                                                                        
    button {                                                                                            
        width: 90%;                                                                                     
    }                                                                                                   
}                                                                                                       
                                                                                                        
@media (max-width: 768px) {                                                                             
    h1 {                                                                                                
        font-size: 1.8em;                                                                               
    }                                                                                                   
                                                                                                        
    nav ul.menu li {                                                                                    
        flex: 1 1 90%;                                                                                  
    }                                                                                                   
                                                                                                        
    button {                                                                                            
        font-size: 1em;                                                                                 
    }                                                                                                   
}                                                                                                       
                                                                                                        
@media (max-width: 480px) {                                                                             
    h1 {                                                                                                
        font-size: 1.6em;                                                                               
    }                                                                                                   
                                                                                                        
    nav ul.menu li a {                                                                                  
        padding: 10px 15px;                                                                             
    }                                                                                                   
                                                                                                        
    button {                                                                                            
        width: 100%;                                                                                    
        font-size: 0.9em;                                                                               
        padding: 10px 20px;                                                                             
    }                                                                                                   
}                                                                                                       
                                                                                                        
/* Рамка для заголовка */                                                                               
.header-border {                                                                                        
    border: 1px solid #00ffff;                                                                          
    padding: 10px;                                                                                      
    border-radius: 8px;                                                                                 
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);                                                          
}                                                                                                       
                                                                                                        
/* Рамка для нижнего меню */                                                                            
.footer-border {                                                                                        
    border: 1px solid #00ffff;                                                                          
    border-radius: 8px;                                                                                 
    box-shadow: 0 -4px 15px rgba(0, 0, 0, 0.5);                                                         
}                                                                                                       
                                                                                                        
additional-menu {
    background-color: #007a99;
}                                                                                                       
                                                                                                        
/* Кнопка возврата наверх */                                                                            
.scroll-to-top {                                                                                        
    position: fixed;                                                                                    
    bottom: 20px;                                                                                       
    right: 20px;                                                                                        
    background-color: #131339;                                                                          
    color: white;                                                                                       
    padding: 10px 15px;                                                                                 
    border-radius: 50%;                                                                                 
    font-size: 1.5em;                                                                                   
    cursor: pointer;                                                                                    
    transition: background-color 0.3s, transform 0.3s;                                                  
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);                                                          
}                                                                                                       
                                                                                                        
.scroll-to-top:hover {                                                                                  
    background-color: #4CAF50;                                                                          
    transform: translateY(-5px);                                                                        
}                                                                                                       
                                                                                                        
/* Анимация при прокрутке */                                                                            
@keyframes headerScrollAnimation {                                                                      
    from {                                                                                              
        opacity: 0;                                                                                     
        transform: translateY(-30px);                                                                   
    }                                                                                                   
    to {                                                                                                
        opacity: 1;                                                                                     
        transform: translateY(0);                                                                       
    }                                                                                                   
}                                                                                                       
                                                                                                        
.header-border {                                                                                        
    animation: headerScrollAnimation 1.5s ease-out;                                                     
} 

section {
    margin: 20px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    text-align: center;
}

section h2, section h3 {
    color: #ffffff;
    margin-bottom: 15px;
}

section p {
    color: #cccccc;
    margin-bottom: 15px;
    line-height: 1.6;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
    text-decoration: none;
    background-color: #131339;
    border-radius: 8px;
    transition: background-color 0.3s, transform 0.3s ease-in-out, box-shadow 0.3s;                     
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);                                                          
    width: 80%;                                                                                         
    max-width: 300px;
}

.btn:hover {
    background-color: #00001a;
    transform: translateY(-5px);
}

.button-group {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
}
                                                                                                        
button:hover {                                                                                          
    transform: translateY(-5px);                                                                        
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);  
}

xuection {
    min-height: 50px;
    width: 100%;
    background-color: #111111;
}
