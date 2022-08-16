import {   
  GraphQLObjectType,
  GraphQLString,
  GraphQLInt,
  GraphQLList,
  GraphQLFloat
 } from 'graphql'


import { fetchAllSearchResults } from '../../utilities/elasticsearch'
import shapeMetadata from '../datasets/shapeMetadata'

export const MetadataType = new GraphQLObjectType({
  name: 'metadataData',
  fields: {
    cell_id: { type: GraphQLString },
    age: { type: GraphQLString },
    sex: { type: GraphQLString },
  },
});

export const fetchMetadataDetails = async (ctx) => {
  //const response = await ctx.database.elastic.search({

  const hits = await fetchAllSearchResults(ctx.database.elastic, {
    index: 'metadata',
    //type: '_doc',
    size: 1000,
    body: {
      query : {
        bool: {
          filter: [
            //{term: { time_point: time_point}},
            //{term: { genotype1: genotype1}},
            //{term: { genotype2: genotype2}},
            //{term: { sex: sex}},
            { range: { [`age`]: { lt: 1000 } } },
          ]
        },
      },
    },
  })

  //const doc = response.hits._source[0]
  console.log(hits)
  
  const data = hits.map(shapeMetadata())
  console.log(data)


  //return doc ? doc._source : null // eslint-disable-line no-underscore-dangle
  return data

}
