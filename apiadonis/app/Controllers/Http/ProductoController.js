'use strict'

const producto = use('App/Models/Producto');

class ProductoController {
    async newproducto({request, response}){
        try{
            const data = await request.all();//peticion
            const product = new producto();

            product.nombre = data.nombre;
            product.Inf_Producto = data.Inf_Producto;

           

            if (await product.save()){
                return response.status(200).json(product);
            }
            
    
    
        } catch (error){
            return error;
        }
    }
    
}

module.exports = ProductoController

