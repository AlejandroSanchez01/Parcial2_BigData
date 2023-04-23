import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Data Catalog table
DataCatalogtable_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="noticias",
    table_name="periodico_elespectador",
    transformation_ctx="DataCatalogtable_node1",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1682209871174 = glueContext.create_dynamic_frame.from_catalog(
    database="noticias",
    table_name="periodico_eltiempo",
    transformation_ctx="AWSGlueDataCatalog_node1682209871174",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=DataCatalogtable_node1,
    mappings=[
        ("col1", "string", "categoria", "string"),
        ("col2", "string", "link", "string"),
        ("col0", "string", "titulo", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node Change Schema
ChangeSchema_node1682209941236 = ApplyMapping.apply(
    frame=AWSGlueDataCatalog_node1682209871174,
    mappings=[
        ("col1", "string", "categoria", "string"),
        ("col2", "string", "link", "string"),
        ("col0", "string", "titulo", "string"),
    ],
    transformation_ctx="ChangeSchema_node1682209941236",
)

# Script generated for node Data Catalog table
DataCatalogtable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=ApplyMapping_node2,
    database="noticias-cloud9",
    table_name="bdnoticias_elespectador",
    transformation_ctx="DataCatalogtable_node3",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1682209967088 = glueContext.write_dynamic_frame.from_catalog(
    frame=ChangeSchema_node1682209941236,
    database="noticias-cloud9",
    table_name="bdnoticias_eltiempo",
    transformation_ctx="AWSGlueDataCatalog_node1682209967088",
)

job.commit()
