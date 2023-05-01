import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as cloudfrontOrigins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class ChalStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    const vpc = new ec2.Vpc(this, 'VPC', {
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'public',
          subnetType: ec2.SubnetType.PUBLIC
        },
        {
          cidrMask: 24,
          name: 'monitoring',
          subnetType: ec2.SubnetType.PUBLIC
        },
      ]
    });

    const trustedAdminCIDRv4 : { cidr: string }[] = this.node.tryGetContext('ctf-chals/trusted-admin-ip-cidrv4');
    const trustedAdminPrefixList = new ec2.CfnPrefixList(this, 'trustedAdminPrefixList', {
      prefixListName: 'CTFPlatformTrustedAdminPrefixList',
      addressFamily: 'IPv4',
      maxEntries: 10,
      entries: trustedAdminCIDRv4,
    });

    const chalSg = new ec2.SecurityGroup(this, 'challenges', { vpc });
    
    chalSg.connections.allowFrom(
      ec2.Peer.prefixList(trustedAdminPrefixList.attrPrefixListId), 
      new ec2.Port({ protocol: ec2.Protocol.ALL, stringRepresentation: '' }),
      'allow from trusted ip');

    const chalLoadBalancerSg = new ec2.SecurityGroup(this, 'challengesLoadBalancer', { vpc });
  
    chalLoadBalancerSg.connections.allowFrom(
      ec2.Peer.prefixList(trustedAdminPrefixList.attrPrefixListId), 
      new ec2.Port({ protocol: ec2.Protocol.ALL, stringRepresentation: '' }),
      'allow from trusted ip');
    
    chalSg.connections.allowFrom(
      chalLoadBalancerSg,
      new ec2.Port({ protocol: ec2.Protocol.ALL, stringRepresentation: '' }),
      'allow from load balancer');
  
  }
}
