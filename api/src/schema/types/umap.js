import {   
  GraphQLObjectType,
  GraphQLString,
  GraphQLInt,
  GraphQLList,
  GraphQLFloat
 } from 'graphql'


import { fetchAllSearchResults } from '../../utilities/elasticsearch'
import shapeUmapData from '../datasets/shapeUmapData'

export const umapType = new GraphQLObjectType({
  name: 'umapData',
  fields: {
    cell_id: { type: GraphQLString },
    dataset: { type: GraphQLString },
    cell_type: { type: GraphQLString },    
    umap_1: { type: GraphQLFloat },
    umap_2: { type: GraphQLFloat }
  },
});

export const fetchUmapData = async (ctx, dataset) => {
  //const response = await ctx.database.elastic.search({

  const hits = await fetchAllSearchResults(ctx.database.elastic, {
    index: 'umap_data',
    //type: '_doc',
    size: 100,
    body: {
      query : {
        bool: {
          filter: [
            {term: { dataset: dataset}},
            //{ range: { [`umap_1`]: { lt: 100 } } },
          ]
        },
      },
    },
  })

  //const doc = response.hits._source[0]
  console.log(hits)
  
  const data = hits.map(shapeUmapData())
  console.log(data)


  //return doc ? doc._source : null // eslint-disable-line no-underscore-dangle
  return data

}