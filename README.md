# Análisis de vibraciones para predecir daños estructurales en construcciones

## Resumen	

El presente proyecto pretende predecir los posibles daños estructurales que pueden presentar diversas construcciones con base en la medición de las vibraciones que estas presentan, por diversas causas como temblores, viento, incluso el mismo medio que las rodea.  Partimos del hecho que un cuerpo capaz de vibrar, es sometido a la acción de una fuerza periódica, cuyo periodo de vibración coincide con el periodo de vibración característico de dicho cuerpo. En estas circunstancias el cuerpo vibra, aumentando de forma progresiva la amplitud del movimiento tras cada una de las actuaciones sucesivas de la fuerza. Este efecto puede ser destructivo en algunos materiales rígidos.


## Objetivos específicos	

- Construir un sistema capaz de medir las vibraciones de diferentes estructuras.
- Analizar los datos obtenidos para determinar si las vibraciones están cerca del punto de resonancia de los materiales
- Emitir alertas cuando las condiciones críticas se cumplan


## Introducción

De acuerdo con [^1], el tránsito de vehículos genera ondas superficiales que se propagan hasta distancias relativamente cortas y en ocasiones sacuden las construcciones aledañas a la vía. El impacto producido por los vehículos depende de su peso y de la velocidad con que se desplazan. La carga de impacto genera ondas superficiales de diferente frecuencia. Así mismo, la condición local conformada por el pavimento y el suelo confieren particularidades al impacto.

[^1]: Sarria A. (2004), Investigación no destructiva y cargas extremas en estructuras. Bogotá: Eiciones Uniandes.

Por otro lado [^2] modeló el paso de un vehículo de dos ejes, cercano a una estructura o vivienda unifamiliar de dos pisos.

De acuerdo con este estudio dos situaciones podrían ocurrir: para un edificio cimentado sobre suelo blando (en el cual no ocurre deformación en la estructura) la respuesta estructural global es dominada por cinemática de cuerpo rígido mientras que si el suelo es rígido con respecto a la estructura, las paredes se deforman de una manera cuasiestática, siguiendo el movimiento del suelo.

[^2]: Francois L. P. (2007), The influence of dynamic soil-structure interaction on traffic induced vibrations in buildings. Soil Dynamics and Earthquake Engineering , 655-674.

### Definición de límites para evitar daños

De forma general los criterios que definen umbrales de vibración que pueden causar daño estructural, no solo dependen de la vibración, también están sujetos a la carga estructural, características de los materiales, a las características dinámicas, a la amplitud de excitación y a la frecuencia sensible. Autoridades de estandarización en el mundo entero, han definido directrices sobre niveles permisibles de la vibración en suelos con afectación a edificios (Normas ISO 2631, ISO 6897 y DIN 4150). En las normas y literatura disponible, se ha trabajado tradicionalmente con los criterios de aceleración y velocidad de partículas en la definición de los valores límites para evitar daños en sistemas estructurales. 

El concepto de daño es relativo dado que puede involucrar desde la generación de micro fisuras hasta la aparición de grietas que puedan inducir algún tipo de colapso. Adicionalmente la aparición o no de daños, grietas y fisuras está íntimamente relacionada con la calidad de los materiales y de las técnicas constructivas. Por esta razón un estudio específico de daños en una edificación particular requeriría de evaluaciones detalladas que van desde la caracterización del suelo y los materiales usados en la construcción hasta la evaluación de las cargas actuantes (vibraciones debidas a tráfico, voladuras, cargas muertas, vivas, viento, etc).

No obstante, las normas internacionales han establecido unos valores de velocidad límite de las partículas del suelo (asociadas con vibraciones) por encima de los cuales es probable que se generen daños visibles en los elementos de una edificación. Sin embargo hay que recordar que estos valores son indicativos. Teniendo en cuenta lo anterior, la norma DIN 4150, establece los valores máximos de velocidad de vibración (en mm/s) en función de la frecuencia, para que no se observan daños en diferentes tipos de edificaciones (comercial, viviendas, edificios, industrias). 

**Tabla 1** : Valores Máximos de Velocidad de partícula (mm/s) para evitar daños (Norma DIN 4150)

|Tipo de Edificación | Frecuencia < 10 Hz| Frecuencia  10-50 Hz| Frecuencia 50-100 Hz|
|----------------|----------------------|----------------------|--------------------------|
|Estructuras delicadas, muy sensibles a la vibración | 3|3-8|8-10|
|Viviendas y Edificios|5|5-15|15-20|
|Comercial e Inductrial|20|20-40|40-50|

## Desarrollo del proyecto 

A continuación se expone de manera general las diferentes etapas que componen el proyecto.

**Hardaware y oonexiones necesarias**

Los componenetes necesarios para realizar este proyecto son:

1. Raspberry Pi 4
2. Sensor de vibración MPU6050 (2)
3. Sensor de vibración ADXL345 (1)

**Diagrama de conexiones**

![Esta es una imagen de ejemplo](https://github.com/kaansau/Vibraciones/blob/main/imagenes/conexion%20raspberry.png)
