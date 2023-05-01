import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as cloudfrontOrigins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as iam from 'aws-cdk-lib/aws-iam';

export class ChalFileServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const filesBucket = new s3.Bucket(this, 'FilesBucket', {
      enforceSSL: true,
      accessControl: s3.BucketAccessControl.PRIVATE,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const originAccessIdentity = new cloudfront.OriginAccessIdentity(this, 'OriginAccessIdentity');
    filesBucket.addToResourcePolicy(new iam.PolicyStatement({
      actions: ['s3:GetObject'],
      resources: [filesBucket.arnForObjects('*')],
      principals: [originAccessIdentity.grantPrincipal],
    }));

    const cfDistributionCertArn = this.node.tryGetContext('ctf-chals/cf-certificate-arn');
    let cfCert = undefined; 
    if (cfDistributionCertArn) {
      cfCert = acm.Certificate.fromCertificateArn(this, "cfDistributionCert", cfDistributionCertArn);
    }

    const cfWebAclId = this.node.tryGetContext('ctf-chals/cfWebAclId');
    const cfDomainNames : string[] = this.node.tryGetContext('ctf-chals/cf-domain-names');

    const staticSiteResponseHeadersPolicyProps = {
      comment: 'Static site response header policy',
      customHeadersBehavior: {
        customHeaders: [
          { header: 'Server', value: 'CloudFront', override: true },
          // { header: 'Cross-Origin-Opener-Policy', value: 'same-origin', override: true },
          // { header: 'Cross-Origin-Resource-Policy', value: 'same-origin', override: true },

          // https://developer.chrome.com/en/docs/privacy-sandbox/permissions-policy/
          { header: 'Permissions-Policy', value: 'fullscreen=()', override: true },

          { header: 'Content-Disposition', value: 'attachment', override: true },

          // Expect-CT, Cross-Origin-Embedder-Policy
        ],
      },
      securityHeadersBehavior: {
        contentSecurityPolicy: { contentSecurityPolicy: "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none';", override: true },
        contentTypeOptions: { override: true },
        frameOptions: { frameOption: cloudfront.HeadersFrameOption.DENY, override: true },
        referrerPolicy: { referrerPolicy: cloudfront.HeadersReferrerPolicy.NO_REFERRER, override: true },
        strictTransportSecurity: { accessControlMaxAge: cdk.Duration.seconds(63072000), includeSubdomains: false, override: true },
      },
    };
    const staticSiteResponseHeadersPolicy = new cloudfront.ResponseHeadersPolicy(this, 'staticSiteResponseHeadersPolicy', staticSiteResponseHeadersPolicyProps);

    const distribution = new cloudfront.Distribution(this, 'Distribution', {
      comment: 'HKCERT CTF 2022 files.hkcert22.pwnable.hk',
      domainNames: cfDomainNames,
      certificate: cfCert,
      priceClass: cloudfront.PriceClass.PRICE_CLASS_200,
      minimumProtocolVersion: cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
      defaultRootObject: 'index.html',
      webAclId: cfWebAclId,
      defaultBehavior: {
        allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD,
        cachePolicy: new cloudfront.CachePolicy(this, 'staticCachePolicy', {
          comment: 'Managed-CachingOptimized but disable gzip',
          defaultTtl: cdk.Duration.days(1),
          minTtl: cdk.Duration.seconds(1),
          maxTtl: cdk.Duration.days(365),
          cookieBehavior: cloudfront.CacheCookieBehavior.none(),
          headerBehavior: cloudfront.CacheHeaderBehavior.none(),
          queryStringBehavior: cloudfront.CacheQueryStringBehavior.none(),
          enableAcceptEncodingGzip: false,
          enableAcceptEncodingBrotli: true,
        }),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        originRequestPolicy: undefined,
        responseHeadersPolicy: staticSiteResponseHeadersPolicy,
        origin: new cloudfrontOrigins.S3Origin(filesBucket, { originAccessIdentity }),
      },
    });

    
  }
}
