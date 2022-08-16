import {   
  GraphQLObjectType,
  GraphQLString,
  GraphQLInt,
  GraphQLList,
  GraphQLFloat
 } from 'graphql'


import { fetchAllSearchResults } from '../../utilities/elasticsearch'
import shapeExpression from '../datasets/shapeExpression'

export const expressionType = new GraphQLObjectType({
  name: 'expressionData',
  fields: {
    cell_id: { type: GraphQLString },
    gene_id: { type: GraphQLString },
    normalized_count: { type: GraphQLFloat }    
  },
});

export const fetchExpressionData = async (ctx, gene) => {
  //const response = await ctx.database.elastic.search({

  const hits = await fetchAllSearchResults(ctx.database.elastic, {
    index: 'expression_data',
    //type: '_doc',
    size: 1000,
    body: {
      query : {
        bool: {
          filter: [
            {term: { gene_id: gene}},
            //{ range: { [`umap_1`]: { lt: 100 } } },
          ]
        },
      },
    },
  })

  //const doc = response.hits._source[0]
  console.log(hits)
  
  const data = hits.map(shapeExpression())
  console.log(data)


  //return doc ? doc._source : null // eslint-disable-line no-underscore-dangle
  return data

}