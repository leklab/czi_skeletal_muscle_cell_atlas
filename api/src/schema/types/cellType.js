import {   
  GraphQLObjectType,
  GraphQLString,
  GraphQLInt,
  GraphQLList,
  GraphQLFloat
 } from 'graphql'


import { fetchAllSearchResults } from '../../utilities/elasticsearch'
import shapeCellType from '../datasets/shapeCellType'

export const CellTypeType = new GraphQLObjectType({
  name: 'cellTypeData',
  fields: {
    cell_id: { type: GraphQLString },
    bbknn_type: { type: GraphQLString },
    harmony_type: { type: GraphQLString },
    scanorama_type: { type: GraphQLString },
  },
});

export const fetchCellTypeDetails = async (ctx) => {
  //const response = await ctx.database.elastic.search({

  const hits = await fetchAllSearchResults(ctx.database.elastic, {
    index: 'cell_type',
    //type: '_doc',
    size: 100,
    body: {
      query : {
        bool: {
          filter: [
            //{term: { cell_id: cell_id}},
            //{term: { genotype1: genotype1}},
            //{term: { genotype2: genotype2}},
            //{term: { sex: sex}},
            { range: { [`cell_id`]: { lt: 1000 } } },
          ]
        },
      },
    },
  })

  //const doc = response.hits._source[0]
  console.log(hits)
  
  const data = hits.map(shapeCellType())
  console.log(data)


  //return doc ? doc._source : null // eslint-disable-line no-underscore-dangle
  return data

}