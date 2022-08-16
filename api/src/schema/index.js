
import {
  GraphQLInt,
  GraphQLList,
  GraphQLNonNull,
  GraphQLObjectType,
  GraphQLSchema,
  GraphQLString,
  GraphQLFloat
} from 'graphql'



import {MetadataType, fetchMetadataDetails} from './types/metadata'
import {umapType, fetchUmapData} from './types/umap'
import {expressionType, fetchExpressionData} from './types/expression'

const rootType = new GraphQLObjectType({
  name: 'Root',
  description: `
The fields below allow for different ways to look up RC2 data.
  `,
  fields: () => ({

    umap : {
      description: 'Retrieve UMAP data',
      type: new GraphQLList(umapType),

      args: {
        dataset: { type: GraphQLString },
      },
      resolve: (obj, args, ctx) => {
        return fetchUmapData(ctx,args.dataset)
      },
    },

    expression : {
      description: 'Retrieve gene expression data',
      type: new GraphQLList(expressionType),

      args: {
        gene: { type: GraphQLString },
      },
      resolve: (obj, args, ctx) => {
        return fetchExpressionData(ctx,args.gene)
      },
    },

    metadata_point : {
      description: 'Look up Metadata',
      type: new GraphQLList(MetadataType),

      args: {
        cell_id: { type: GraphQLString },
        age: { type: GraphQLString },
        sex: { type: GraphQLString },
      },
      resolve: (obj, args, ctx) => {
        return fetchMetadataDetails(ctx)
      },
    },

  }),
})

const Schema = new GraphQLSchema({
  query: rootType,
  types: [MetadataType] 
  //types: datasetSpecificTypes,
})

export default Schema