//import express from 'express'
//import elasticsearch from 'elasticsearch'
//import graphQLHTTP from 'express-graphql'
//import Redis from 'ioredis'
//import serveStatic from 'serve-static'
//import pcgcSchema from './pcgc_schema'


//var elasticsearch = require('elasticsearch')
//var express = require('express');
//var graphQLHTTP = require('express-graphql');
//var { buildSchema } = require('graphql');

import { MongoClient } from 'mongodb'
import elasticsearch from 'elasticsearch'
import graphQLHTTP from 'express-graphql'
import express from 'express'
import pcgcSchema from './schema'
import cors from 'cors'
import compression from 'compression'


const app = express()
app.use(compression())
app.use(cors())

// Construct a schema, using GraphQL schema language
/*
var schema = buildSchema(`
  type Query {
    hello: String
  }
`);
*/



// The root provides a resolver function for each API endpoint
/*
var root = {
  hello: () => {
    return 'Hello world!';
  },
};
*/


// eslint-disable-line prettier/prettier
;(async () => {
  try {

    /*
    const mongoClient = await MongoClient.connect("mongodb://localhost:27017/rc2", {
      useNewUrlParser: true, useUnifiedTopology: true
    })*/

    const elastic = new elasticsearch.Client({
      apiVersion: '5.6',
      host: "http://localhost:9200",
    })

    app.use(
      [/^\/$/, /^\/api\/?$/],
      graphQLHTTP({
        schema: pcgcSchema,
        //rootValue: root,
        graphiql: true,
        context: {
          database: {
            elastic,
            //mouse_db: mongoClient.db()
          },
        },
      })
    )

    app.get('/health', (req, res) => {
      res.json({})
    })

    app.listen(4001, () => {
      console.log(`Listening on 4001`)
    })
  } catch (error) {
    console.log(error)
  }
})()






/*
var express = require('express');
var graphqlHTTP = require('express-graphql');
var { buildSchema } = require('graphql');

// Construct a schema, using GraphQL schema language
var schema = buildSchema(`
  type Query {
    hello: String
  }
`);

// The root provides a resolver function for each API endpoint
var root = {
  hello: () => {
    return 'Hello world!';
  },
};

var app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true,
}));
app.listen(4000,'0.0.0.0');
console.log('Running a GraphQL API server at http://0.0.0.0:4000/graphql');
*/
