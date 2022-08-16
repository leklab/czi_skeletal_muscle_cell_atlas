import {   
  GraphQLObjectType,
  GraphQLString,
  GraphQLInt,
  GraphQLList,
  GraphQLFloat
 } from 'graphql'


import { fetchAllSearchResults } from '../../utilities/elasticsearch'
import shapeBBKNN from '../datasets/shapeBBKNN'

export const BBKNNType = new GraphQLObjectType({
  name: 'bbknnData',
  fields: {
    cell_id: { type: GraphQLString },
    x_value: { type: GraphQLFloat },
    y_value: { type: GraphQLFloat },
  },
});

export const fetchBBKNNDetails = async (ctx) => {
  //const response = await ctx.database.elastic.search({

  const hits = await fetchAllSearchResults(ctx.database.elastic, {
    index: 'bbknn',
    //type: '_doc',
    size: 100,
    body: {
      query : {
        bool: {
          filter: [
            //{term: { time_point: time_point}},
            //{term: { genotype1: genotype1}},
            //{term: { genotype2: genotype2}},
            //{term: { sex: sex}},
            { range: { [`x_value`]: { lt: 50 } } },
          ]
        },
      },
    },
  })

  //const doc = response.hits._source[0]
  console.log(hits)
  
  const data = hits.map(shapeBBKNN())
  console.log(data)


  //return doc ? doc._source : null // eslint-disable-line no-underscore-dangle
  return data

}