require("dotenv").config();
const express = require("express");
const { ApolloServer, gql } = require("apollo-server-express");
const mongoose = require("mongoose");
const cors = require("cors");

const MONGO_URI = process.env.MONGO_URI;
const PORT = process.env.PORT || 8090;

if (!MONGO_URI) {
  console.log("Falta MONGO_URI en el archivo .env");
  process.exit(1);
}

mongoose
  .connect(MONGO_URI)
  .then(() => console.log("Conectado a MongoDB Atlas"))
  .catch((err) => console.log("Error de conexión:", err.message));

const ProductoModel = mongoose.model(
  "producto",
  new mongoose.Schema({
    nombre: String,
    categoria: String,
    precio: Number,
    disponible: Boolean
  })
);

const PedidoModel = mongoose.model(
  "pedido",
  new mongoose.Schema({
    cliente: String,
    telefono: String,
    total: Number,
    estado: String
  })
);

const typeDefs = gql`
  type Producto {
    id: ID!
    nombre: String
    categoria: String
    precio: Int
    disponible: Boolean
  }

  type Pedido {
    id: ID!
    cliente: String
    telefono: String
    total: Int
    estado: String
  }

  input ProductoInput {
    nombre: String
    categoria: String
    precio: Int
    disponible: Boolean
  }

  input PedidoInput {
    cliente: String
    telefono: String
    total: Int
  }

  type Query {
    getProductos: [Producto]
    getProducto(id: ID!): Producto
    getPedidos: [Pedido]
  }

  type Mutation {
    addProducto(input: ProductoInput): Producto
    updateProducto(id: ID!, input: ProductoInput): Producto
    deleteProducto(id: ID!): String
    addPedido(input: PedidoInput): Pedido
  }
`;

const resolvers = {
  Query: {
    getProductos: async () => await ProductoModel.find(),
    getProducto: async (_, { id }) => await ProductoModel.findById(id),
    getPedidos: async () => await PedidoModel.find()
  },
  Mutation: {
    addProducto: async (_, { input }) => {
      const nuevo = new ProductoModel(input);
      return await nuevo.save();
    },
    updateProducto: async (_, { id, input }) => {
      return await ProductoModel.findByIdAndUpdate(id, input, { new: true });
    },
    deleteProducto: async (_, { id }) => {
      await ProductoModel.findByIdAndDelete(id);
      return "Producto eliminado";
    },
    addPedido: async (_, { input }) => {
      const nuevo = new PedidoModel({ ...input, estado: "pendiente" });
      return await nuevo.save();
    }
  }
};

async function iniciarServidor() {
  const server = new ApolloServer({ typeDefs, resolvers });
  await server.start();

  const app = express();
  app.use(cors());
  server.applyMiddleware({ app });

  app.listen(PORT, () => {
    console.log("GraphQL iniciado en http://localhost:" + PORT + server.graphqlPath);
  });
}

iniciarServidor();